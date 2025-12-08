\layout {
    \context { \Lyrics
        early-font-allographs = #'((m-final . auto))
    }
}

actual =\relative g' { \repeat unfold 30 g } \addlyrics {
    am em im om um ym % all
    am* em* im* om* um* ym* % none
    mam mamm mam. mam, mam! mam? mam; % all
    mam -- mim -- mum % only 'mum'
    "am mem" "am, mem!" % all last -m
    "am* mem*" "am*, mem*!"
    "mam*mem"
}
