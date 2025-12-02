\layout {
    \context { \Lyrics
        early-font-allographs = #'((m-final . auto))
    }
}

actual = \relative g' { \repeat unfold 30 {g} }

\addlyrics {
    am em im om um ym
    am* em* im* om* um* ym*
    mam mamm mam. mam, mam! mam? mam;
    mam -- mim -- mum
    "am mem" "am, mem!"
    am*mem
    "am* m*em*"
    oru[m] or[um] orum
    oru{m} oru{m*}
}
