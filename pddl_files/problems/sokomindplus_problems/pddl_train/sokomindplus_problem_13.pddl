(define (problem sokomindplus_problem)
  (:domain sokomindplus)
  (:objects
        r - robot
        b0 - obj
        b1 - obj
        b2 - obj
        b3 - obj
        b4 - obj
        b5 - obj
        b6 - obj
        b7 - obj
        b8 - obj
        b9 - obj
        b10 - obj
        b11 - obj
        b12 - obj
        b13 - obj
        b14 - obj
        b15 - obj
        b16 - obj
        p0 - pos
        p1 - pos
        p2 - pos
        p3 - pos
        p4 - pos
        p5 - pos
        p6 - pos
        p7 - pos
        p8 - pos
        p9 - pos
        p10 - pos
        p11 - pos
        p12 - pos
        p13 - pos
        p14 - pos
        p15 - pos
        p16 - pos
        p17 - pos
        p18 - pos
        p19 - pos
        p20 - pos
        p21 - pos
        p22 - pos
        p23 - pos
        p24 - pos
        p25 - pos
        p26 - pos
        p27 - pos
        p28 - pos
        p29 - pos
        p30 - pos
        p31 - pos
        p32 - pos
        p33 - pos
        p34 - pos
        p35 - pos
        p36 - pos
        p37 - pos
        p38 - pos
        p39 - pos
        p40 - pos
        p41 - pos
        p42 - pos
        p43 - pos
        p44 - pos
        p45 - pos
        p46 - pos
        p47 - pos
        p48 - pos
        p49 - pos
        p50 - pos
        p51 - pos
        p52 - pos
        p53 - pos
        p54 - pos
        p55 - pos
        p56 - pos
        p57 - pos
        p58 - pos
        p59 - pos
        p60 - pos
        p61 - pos
        p62 - pos
        p63 - pos
        p64 - pos
        p65 - pos
        p66 - pos
        p67 - pos
        p68 - pos
        p69 - pos
        p70 - pos
        p71 - pos
        p72 - pos
        p73 - pos
        p74 - pos
        p75 - pos
        p76 - pos
        p77 - pos
        p78 - pos
        p79 - pos
        p80 - pos
        p81 - pos
        p82 - pos
        p83 - pos
        p84 - pos
        p85 - pos
        p86 - pos
        p87 - pos
        p88 - pos
        p89 - pos
        p90 - pos
        p91 - pos
        p92 - pos
        p93 - pos
        p94 - pos
        p95 - pos
        p96 - pos
        p97 - pos
        p98 - pos
        p99 - pos
  )
  (:init
        (rAt r p25)
        (oAt b0 p70)
        (isBox b0)
        (oAt b1 p2)
        (isBox b1)
        (oAt b2 p48)
        (isBox b2)
        (oAt b3 p28)
        (isBox b3)
        (oAt b4 p78)
        (isBox b4)
        (oAt b5 p99)
        (isBox b5)
        (oAt b6 p21)
        (isBox b6)
        (oAt b7 p29)
        (isBox b7)
        (oAt b8 p19)
        (isBox b8)
        (oAt b9 p53)
        (isBox b9)
        (oAt b10 p24)
        (isBox b10)
        (oAt b11 p31)
        (isBox b11)
        (oAt b12 p87)
        (isBox b12)
        (oAt b13 p80)
        (isBox b13)
        (oAt b14 p15)
        (isBox b14)
        (oAt b15 p59)
        (isBox b15)
        (oAt b16 p61)
        (isBox b16)
        (posEmpty p0)
        (posEmpty p1)
        (posEmpty p6)
        (posEmpty p9)
        (posEmpty p12)
        (posEmpty p14)
        (posEmpty p16)
        (posEmpty p17)
        (posEmpty p20)
        (posEmpty p22)
        (posEmpty p25)
        (posEmpty p27)
        (posEmpty p30)
        (posEmpty p32)
        (posEmpty p33)
        (posEmpty p34)
        (posEmpty p35)
        (posEmpty p37)
        (posEmpty p40)
        (posEmpty p41)
        (posEmpty p42)
        (posEmpty p44)
        (posEmpty p47)
        (posEmpty p49)
        (posEmpty p51)
        (posEmpty p52)
        (posEmpty p54)
        (posEmpty p55)
        (posEmpty p56)
        (posEmpty p57)
        (posEmpty p58)
        (posEmpty p60)
        (posEmpty p63)
        (posEmpty p66)
        (posEmpty p68)
        (posEmpty p69)
        (posEmpty p74)
        (posEmpty p75)
        (posEmpty p76)
        (posEmpty p79)
        (posEmpty p81)
        (posEmpty p82)
        (posEmpty p83)
        (posEmpty p84)
        (posEmpty p85)
        (posEmpty p86)
        (posEmpty p88)
        (posEmpty p89)
        (posEmpty p94)
        (posEmpty p95)
        (posEmpty p96)
        (posEmpty p97)
        (rightTo p1 p0)
        (leftTo p0 p1)
        (leftTo p0 p1)
        (rightTo p1 p0)
        (rightTo p2 p1)
        (leftTo p1 p2)
        (downTo p12 p2)
        (upTo p2 p12)
        (leftTo p1 p2)
        (rightTo p2 p1)
        (downTo p16 p6)
        (upTo p6 p16)
        (downTo p19 p9)
        (upTo p9 p19)
        (upTo p2 p12)
        (downTo p12 p2)
        (downTo p22 p12)
        (upTo p12 p22)
        (downTo p24 p14)
        (upTo p14 p24)
        (rightTo p15 p14)
        (leftTo p14 p15)
        (downTo p25 p15)
        (upTo p15 p25)
        (leftTo p14 p15)
        (rightTo p15 p14)
        (rightTo p16 p15)
        (leftTo p15 p16)
        (upTo p6 p16)
        (downTo p16 p6)
        (leftTo p15 p16)
        (rightTo p16 p15)
        (rightTo p17 p16)
        (leftTo p16 p17)
        (downTo p27 p17)
        (upTo p17 p27)
        (leftTo p16 p17)
        (rightTo p17 p16)
        (upTo p9 p19)
        (downTo p19 p9)
        (downTo p29 p19)
        (upTo p19 p29)
        (downTo p30 p20)
        (upTo p20 p30)
        (rightTo p21 p20)
        (leftTo p20 p21)
        (downTo p31 p21)
        (upTo p21 p31)
        (leftTo p20 p21)
        (rightTo p21 p20)
        (rightTo p22 p21)
        (leftTo p21 p22)
        (upTo p12 p22)
        (downTo p22 p12)
        (downTo p32 p22)
        (upTo p22 p32)
        (leftTo p21 p22)
        (rightTo p22 p21)
        (upTo p14 p24)
        (downTo p24 p14)
        (downTo p34 p24)
        (upTo p24 p34)
        (rightTo p25 p24)
        (leftTo p24 p25)
        (upTo p15 p25)
        (downTo p25 p15)
        (downTo p35 p25)
        (upTo p25 p35)
        (leftTo p24 p25)
        (rightTo p25 p24)
        (upTo p17 p27)
        (downTo p27 p17)
        (downTo p37 p27)
        (upTo p27 p37)
        (rightTo p28 p27)
        (leftTo p27 p28)
        (leftTo p27 p28)
        (rightTo p28 p27)
        (rightTo p29 p28)
        (leftTo p28 p29)
        (upTo p19 p29)
        (downTo p29 p19)
        (leftTo p28 p29)
        (rightTo p29 p28)
        (upTo p20 p30)
        (downTo p30 p20)
        (downTo p40 p30)
        (upTo p30 p40)
        (rightTo p31 p30)
        (leftTo p30 p31)
        (upTo p21 p31)
        (downTo p31 p21)
        (downTo p41 p31)
        (upTo p31 p41)
        (leftTo p30 p31)
        (rightTo p31 p30)
        (rightTo p32 p31)
        (leftTo p31 p32)
        (upTo p22 p32)
        (downTo p32 p22)
        (downTo p42 p32)
        (upTo p32 p42)
        (leftTo p31 p32)
        (rightTo p32 p31)
        (rightTo p33 p32)
        (leftTo p32 p33)
        (leftTo p32 p33)
        (rightTo p33 p32)
        (rightTo p34 p33)
        (leftTo p33 p34)
        (upTo p24 p34)
        (downTo p34 p24)
        (downTo p44 p34)
        (upTo p34 p44)
        (leftTo p33 p34)
        (rightTo p34 p33)
        (rightTo p35 p34)
        (leftTo p34 p35)
        (upTo p25 p35)
        (downTo p35 p25)
        (leftTo p34 p35)
        (rightTo p35 p34)
        (upTo p27 p37)
        (downTo p37 p27)
        (downTo p47 p37)
        (upTo p37 p47)
        (upTo p30 p40)
        (downTo p40 p30)
        (rightTo p41 p40)
        (leftTo p40 p41)
        (upTo p31 p41)
        (downTo p41 p31)
        (downTo p51 p41)
        (upTo p41 p51)
        (leftTo p40 p41)
        (rightTo p41 p40)
        (rightTo p42 p41)
        (leftTo p41 p42)
        (upTo p32 p42)
        (downTo p42 p32)
        (downTo p52 p42)
        (upTo p42 p52)
        (leftTo p41 p42)
        (rightTo p42 p41)
        (upTo p34 p44)
        (downTo p44 p34)
        (downTo p54 p44)
        (upTo p44 p54)
        (upTo p37 p47)
        (downTo p47 p37)
        (downTo p57 p47)
        (upTo p47 p57)
        (rightTo p48 p47)
        (leftTo p47 p48)
        (downTo p58 p48)
        (upTo p48 p58)
        (leftTo p47 p48)
        (rightTo p48 p47)
        (rightTo p49 p48)
        (leftTo p48 p49)
        (downTo p59 p49)
        (upTo p49 p59)
        (leftTo p48 p49)
        (rightTo p49 p48)
        (upTo p41 p51)
        (downTo p51 p41)
        (downTo p61 p51)
        (upTo p51 p61)
        (rightTo p52 p51)
        (leftTo p51 p52)
        (upTo p42 p52)
        (downTo p52 p42)
        (leftTo p51 p52)
        (rightTo p52 p51)
        (rightTo p53 p52)
        (leftTo p52 p53)
        (downTo p63 p53)
        (upTo p53 p63)
        (leftTo p52 p53)
        (rightTo p53 p52)
        (rightTo p54 p53)
        (leftTo p53 p54)
        (upTo p44 p54)
        (downTo p54 p44)
        (leftTo p53 p54)
        (rightTo p54 p53)
        (rightTo p55 p54)
        (leftTo p54 p55)
        (leftTo p54 p55)
        (rightTo p55 p54)
        (rightTo p56 p55)
        (leftTo p55 p56)
        (downTo p66 p56)
        (upTo p56 p66)
        (leftTo p55 p56)
        (rightTo p56 p55)
        (rightTo p57 p56)
        (leftTo p56 p57)
        (upTo p47 p57)
        (downTo p57 p47)
        (leftTo p56 p57)
        (rightTo p57 p56)
        (rightTo p58 p57)
        (leftTo p57 p58)
        (upTo p48 p58)
        (downTo p58 p48)
        (downTo p68 p58)
        (upTo p58 p68)
        (leftTo p57 p58)
        (rightTo p58 p57)
        (rightTo p59 p58)
        (leftTo p58 p59)
        (upTo p49 p59)
        (downTo p59 p49)
        (downTo p69 p59)
        (upTo p59 p69)
        (leftTo p58 p59)
        (rightTo p59 p58)
        (downTo p70 p60)
        (upTo p60 p70)
        (rightTo p61 p60)
        (leftTo p60 p61)
        (upTo p51 p61)
        (downTo p61 p51)
        (leftTo p60 p61)
        (rightTo p61 p60)
        (upTo p53 p63)
        (downTo p63 p53)
        (upTo p56 p66)
        (downTo p66 p56)
        (downTo p76 p66)
        (upTo p66 p76)
        (upTo p58 p68)
        (downTo p68 p58)
        (downTo p78 p68)
        (upTo p68 p78)
        (rightTo p69 p68)
        (leftTo p68 p69)
        (upTo p59 p69)
        (downTo p69 p59)
        (downTo p79 p69)
        (upTo p69 p79)
        (leftTo p68 p69)
        (rightTo p69 p68)
        (upTo p60 p70)
        (downTo p70 p60)
        (downTo p80 p70)
        (upTo p70 p80)
        (downTo p84 p74)
        (upTo p74 p84)
        (rightTo p75 p74)
        (leftTo p74 p75)
        (downTo p85 p75)
        (upTo p75 p85)
        (leftTo p74 p75)
        (rightTo p75 p74)
        (rightTo p76 p75)
        (leftTo p75 p76)
        (upTo p66 p76)
        (downTo p76 p66)
        (downTo p86 p76)
        (upTo p76 p86)
        (leftTo p75 p76)
        (rightTo p76 p75)
        (upTo p68 p78)
        (downTo p78 p68)
        (downTo p88 p78)
        (upTo p78 p88)
        (rightTo p79 p78)
        (leftTo p78 p79)
        (upTo p69 p79)
        (downTo p79 p69)
        (downTo p89 p79)
        (upTo p79 p89)
        (leftTo p78 p79)
        (rightTo p79 p78)
        (upTo p70 p80)
        (downTo p80 p70)
        (rightTo p81 p80)
        (leftTo p80 p81)
        (leftTo p80 p81)
        (rightTo p81 p80)
        (rightTo p82 p81)
        (leftTo p81 p82)
        (leftTo p81 p82)
        (rightTo p82 p81)
        (rightTo p83 p82)
        (leftTo p82 p83)
        (leftTo p82 p83)
        (rightTo p83 p82)
        (rightTo p84 p83)
        (leftTo p83 p84)
        (upTo p74 p84)
        (downTo p84 p74)
        (downTo p94 p84)
        (upTo p84 p94)
        (leftTo p83 p84)
        (rightTo p84 p83)
        (rightTo p85 p84)
        (leftTo p84 p85)
        (upTo p75 p85)
        (downTo p85 p75)
        (downTo p95 p85)
        (upTo p85 p95)
        (leftTo p84 p85)
        (rightTo p85 p84)
        (rightTo p86 p85)
        (leftTo p85 p86)
        (upTo p76 p86)
        (downTo p86 p76)
        (downTo p96 p86)
        (upTo p86 p96)
        (leftTo p85 p86)
        (rightTo p86 p85)
        (rightTo p87 p86)
        (leftTo p86 p87)
        (downTo p97 p87)
        (upTo p87 p97)
        (leftTo p86 p87)
        (rightTo p87 p86)
        (rightTo p88 p87)
        (leftTo p87 p88)
        (upTo p78 p88)
        (downTo p88 p78)
        (leftTo p87 p88)
        (rightTo p88 p87)
        (rightTo p89 p88)
        (leftTo p88 p89)
        (upTo p79 p89)
        (downTo p89 p79)
        (downTo p99 p89)
        (upTo p89 p99)
        (leftTo p88 p89)
        (rightTo p89 p88)
        (upTo p84 p94)
        (downTo p94 p84)
        (rightTo p95 p94)
        (leftTo p94 p95)
        (upTo p85 p95)
        (downTo p95 p85)
        (leftTo p94 p95)
        (rightTo p95 p94)
        (rightTo p96 p95)
        (leftTo p95 p96)
        (upTo p86 p96)
        (downTo p96 p86)
        (leftTo p95 p96)
        (rightTo p96 p95)
        (rightTo p97 p96)
        (leftTo p96 p97)
        (upTo p87 p97)
        (downTo p97 p87)
        (leftTo p96 p97)
        (rightTo p97 p96)
        (upTo p89 p99)
        (downTo p99 p89)
  )
  (:goal
        (and
          (oAt b4 p81)
        )
  )
)