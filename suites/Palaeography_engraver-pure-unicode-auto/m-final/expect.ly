%{
    For now, unicode does not support
    the compressed for of final "m".
    For now, I represent it using the "ɜ"
    symbol. This is incorrect and should be avoided
    in the future.
%}
expected = \relative g' { \repeat unfold 30 g }

\addlyrics {
    aɜ eɜ iɜ oɜ uɜ yɜ
    am em im om um ym
    maɜ mamɜ maɜ. maɜ, maɜ! maɜ? maɜ;
    mam -- mim -- muɜ
    "aɜ meɜ" "aɜ, meɜ!"
    aɜmeɜ
    "am ɜem"
    orum orum oruɜ
    oruɜ orum
}
