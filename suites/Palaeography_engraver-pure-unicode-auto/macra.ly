\layout {
    \context { \Lyrics
        \consists #early:Palaeography_engraver
        early-font-config = #'(
         (allographs . #t)
         (ligatures . #t)
        )
        early-font-pure-unicode = ##t
        \consists #print_lyrics
    }
}
