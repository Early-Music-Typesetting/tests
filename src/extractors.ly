%{
    This files contains engravers allowing for
    printing specific score features.

    Include those engravers in the 'output.ly' file
    within a test suite.
%}

#(define-public (print_lyrics context)
  (let ((all-lyrics '()))
   (make-engraver
    (acknowledgers
     ((lyric-syllable-interface engraver grob source)
      (let ((text (ly:grob-property grob 'text)))
       (set! all-lyrics
        (append! all-lyrics (list text))))))
    ((finalize translator)
     (display "__SCHEME_STARTS__\n")
     (display-scheme-music all-lyrics)
     (display "__SCHEME_ENDS__"))
)))
