(require
  hyrule [block case])

(import
  math [ceil]
  sys
  os
  socket
  re
  subprocess
  html
  datetime [datetime timezone]
  time [time ctime sleep]
  pathlib [Path]
  json
  base64
  quopri

  imaplib
  imapclient [IMAPClient SEEN]
  imapclient.response-types
  metadict [MetaDict]
  humanize [naturaldelta]
  setproctitle [setproctitle])

(setv config-path (/
  (Path (get os.environ "XDG_CONFIG_HOME"))
  "charlie_brown.json"))

;; --------------------------------------------------
;; * Helpers
;; --------------------------------------------------

(defn hesc [x]
  (html.escape (if (is (type x) bytes)
    (.decode x "ascii" "backslashreplace")
    (str x))))

(defn kdialog-wrap [max-len text]
  ; Insert spaces into long "words" (passages of non-whitespace
  ; characters). Otherwise, `kdialog` may truncate the entire string.
  (re.sub (.format r"(\S{{{}}})(\S)" max-len) r"\1 \1" text))

(defn info-dialog [text]
  (subprocess.run :check True ["kdialog"
    "--title" "Charlie Brown"
    "--msgbox" text]))

(defn question-dialog [text yes no cancel]
  (setv p (subprocess.run ["kdialog"
    "--title" "Charlie Brown"
    "--yesnocancel" text
    "--yes-label" yes
    "--no-label" no
    "--cancel-label" cancel]))
  (case p.returncode
    0    yes
    1    no
    2    cancel
    else (.check-returncode p)))

(defn show-age [dt]
  (re.sub
    r"\Aan? " "1 "
    (naturaldelta (- (datetime.now timezone.utc) dt))))

(defn msg [#* args]
  (print (+ (ctime) ":") #* args :file sys.stderr))

;; --------------------------------------------------
;; * Interaction with the server
;; --------------------------------------------------

(setv last-idled None)
(setv min-idle-delay-seconds 4)

(defn main-loop []
  (setproctitle "charlie_brown")
  (setv config (MetaDict (json.loads (.read-text config-path))))
  (global last-idled)

  (while True (block :login (try
    (with [server (IMAPClient config.server
        :timeout config.global-timeout-seconds
        :ssl True)]
      (setv server.normalise-times False)
      
      (msg "Logging in")
      (.login server config.username config.password)
      (setv refresh-time (+ (time) (* 60 config.login-interval-minutes)))
      (.select-folder server config.folder-monitor)

      (report server config)

      (while True
        (setv report? False)
        (when (and last-idled (< (- (time) last-idled) min-idle-delay-seconds))
          ; Give it a rest for a moment. We don't need to run this
          ; loop as fast as possible for every server event.
          (msg "Sleeping")
          (sleep (max 1 (ceil
            (- (+ last-idled min-idle-delay-seconds) (time))))))
        (try
          (.idle server)
          (setv last-idled (time))
          (msg "Idling")
          (for [item (.idle-check server :timeout (max 1 (min
              (- refresh-time (time))
              (* 60 config.idle-timeout-minutes))))]
            (when (= (get item 1) b"EXISTS")
              (setv report? True)))
          (finally
            ; Calling `.idle-done` and `.idle` on each iteration
            ; implicitly checks that the connection is still alive. If
            ; it's dead, we'll get `TimeoutError`.
            (.idle-done server)))
        (when (>= (time) refresh-time)
          (block-ret-from :login))
        (when report?
          (report server config))))

    (except [e [TimeoutError imaplib.IMAP4.abort socket.gaierror]]
      (msg (repr e)))))))

(defn report [server config]

  ; Identify the messages we should report.
  (setv already-reported (try
    (json.loads (.read-text (Path config.tempfile)))
    (except [FileNotFoundError]
      [])))
  (setv new (sorted (-
    (set (.search server ["UNSEEN"]))
    (set already-reported))))

  ; Report on new messages and allow the user to take action on them.
  (if (> (len new) config.max-itemized-messages)
    (info-dialog f"Geez, Mr. Popular, you have <b>{(len new)}</b> new messages.")
    (do
      (setv info (.fetch server new [
        "ENVELOPE"
        "BODYSTRUCTURE"]))
      (for [[msg-i msg-id] (enumerate new)]
        (setv summary (message-summary
          server config msg-id (get info msg-id)))
        (setv action (question-dialog
          :text (+
            (if (> (len new) 1)
              f"New message <b>{(+ msg-i 1)}</b> of <b>{(len new)}</b>:<br><br>"
              "New message:<br><br>")
            f"<b>Age:</b> {(hesc (show-age summary.date))}<br>"
            f"<b>From:</b> {(hesc summary.from)}<br>"
            f"<b>Subject:</b> {(hesc summary.subject)}<br><br>"
            (.replace
              (hesc (kdialog-wrap
                config.kdialog-max-word-len
                summary.body-preview))
              "\n" "<br>"))
          :yes "Keep"
          :no "Trash"
          :cancel "Mark Read"))
        (case action
          "Trash" (do
            (.move server msg-id config.folder-trash)
            (.expunge server msg-id))
          "Mark Read"
            (.add-flags server msg-id [SEEN])))))

  ; Log all messages reported.
  (.write-text (Path config.tempfile) (json.dumps (+ already-reported new))))

(defn message-summary [server config msg-id info]
  (setv BASE64-MULTIPLE 4)
  (setv PART-IX-ENCODING 5)
  (setv PART-IX-CHARSET 2)

  (setv envelope (get info b"ENVELOPE"))
  (setv body-struct (get info b"BODYSTRUCTURE"))

  ; Find the MIME part that we want to make the body preview from.
  (defn find-part [matcher]
    (block
      (defn f [key x]
        (if (isinstance (get x 0) list)
          (for [[i e] (enumerate (get x 0))]
            (f (+ key #((+ i 1))) e))
          (when (= (tuple (cut x (len matcher))) matcher)
            (block-ret [key x]))))
      (f #() body-struct)
      None))
  (setv [part-ix part] (or
    (find-part #(b"TEXT" b"PLAIN"))
    (find-part #(b"TEXT" b"HTML"))
    ["TEXT" body-struct]))
  (setv part-ix (or part-ix #("TEXT")))
  (print part)

  ; Make the body preview.
  (setv [body-preview] (gfor
    [k v] (.items (get (.fetch server msg-id (.format
      "BODY.PEEK[{}]<0.{}>"
      (.join "." (map str part-ix))
      config.body-preview-bytes)) msg-id))
    :if (in b"BODY" k)
    v))
  (setv body-preview (re.sub
    "\r(\n)?" "\n"
    (.strip (.decode :errors "replace"
      (case (get part PART-IX-ENCODING)
        ; Decoding is tricky because we have only a prefix of the
        ; body, not necessarily the whole body.
        b"BASE64" (do
          (setv x (re.sub rb"\s" b"" body-preview))
          ; Cut to a multiple of 4 so every chunk can be decoded.
          (base64.b64decode (cut x
            (* BASE64-MULTIPLE (// (len x) BASE64-MULTIPLE)))))
        b"QUOTED-PRINTABLE"
          (quopri.decodestring
            ; Remove any trailing incomplete escapes.
            (re.sub rb"=[^=]?\Z" b"" (.strip body-preview)))
        else
          body-preview)
      :encoding (do
        (setv charset (get part PART-IX-CHARSET))
        (if (and
            (isinstance charset tuple)
            (>= (len charset 2))
            (= (get charset 0) b"CHARSET"))
          (.decode (get charset 1) "ASCII")
          "UTF-8"))))))

  (MetaDict
    :date envelope.date
    :from (get envelope.sender 0)
    :subject (.decode envelope.subject "UTF-8" :errors "replace")
    :body-preview body-preview))
