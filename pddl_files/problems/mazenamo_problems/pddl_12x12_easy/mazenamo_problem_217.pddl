(define (problem mazenamo_problem)
    (:domain mazenamo)
    (:objects
		r - robot
		p0 - pos
		o1 - obstacle
		p1 - pos
		o2 - obstacle
		p2 - pos
		o3 - obstacle
		p3 - pos
		o4 - obstacle
		p4 - pos
		o5 - obstacle
		p5 - pos
		o6 - obstacle
		p6 - pos
		o7 - obstacle
		p7 - pos
		o8 - obstacle
		p8 - pos
		o9 - obstacle
		p9 - pos
		o10 - obstacle
		p10 - pos
		o11 - obstacle
		p11 - pos
		o12 - obstacle
		p12 - pos
		o13 - obstacle
		p13 - pos
		p14 - pos
		p15 - pos
		o16 - obstacle
		p16 - pos
		p17 - pos
		o18 - obstacle
		p18 - pos
		o19 - obstacle
		p19 - pos
		o20 - obstacle
		p20 - pos
		p21 - pos
		p22 - pos
		o23 - obstacle
		p23 - pos
		o24 - obstacle
		p24 - pos
		o25 - obstacle
		p25 - pos
		o26 - obstacle
		p26 - pos
		p27 - pos
		p28 - pos
		o29 - obstacle
		p29 - pos
		p30 - pos
		p31 - pos
		p32 - pos
		p33 - pos
		p34 - pos
		p35 - pos
		o36 - obstacle
		p36 - pos
		o37 - obstacle
		p37 - pos
		p38 - pos
		p39 - pos
		o40 - obstacle
		p40 - pos
		p41 - pos
		o42 - obstacle
		p42 - pos
		o43 - obstacle
		p43 - pos
		o44 - obstacle
		p44 - pos
		p45 - pos
		o46 - obstacle
		p46 - pos
		p47 - pos
		o48 - obstacle
		p48 - pos
		o49 - obstacle
		p49 - pos
		o50 - obstacle
		p50 - pos
		p51 - pos
		p52 - pos
		p53 - pos
		o54 - obstacle
		p54 - pos
		p55 - pos
		o56 - obstacle
		p56 - pos
		o57 - obstacle
		p57 - pos
		o58 - obstacle
		p58 - pos
		o59 - obstacle
		p59 - pos
		o60 - obstacle
		p60 - pos
		o61 - obstacle
		p61 - pos
		p62 - pos
		o63 - obstacle
		p63 - pos
		o64 - obstacle
		p64 - pos
		o65 - obstacle
		p65 - pos
		o66 - obstacle
		p66 - pos
		o67 - obstacle
		p67 - pos
		p68 - pos
		p69 - pos
		o70 - obstacle
		p70 - pos
		o71 - obstacle
		p71 - pos
		o72 - obstacle
		p72 - pos
		o73 - obstacle
		p73 - pos
		o74 - obstacle
		p74 - pos
		o75 - obstacle
		p75 - pos
		o76 - obstacle
		p76 - pos
		o77 - obstacle
		p77 - pos
		o78 - obstacle
		p78 - pos
		o79 - obstacle
		p79 - pos
		o80 - obstacle
		p80 - pos
		p81 - pos
		p82 - pos
		o83 - obstacle
		p83 - pos
		o84 - obstacle
		p84 - pos
		o85 - obstacle
		p85 - pos
		o86 - obstacle
		p86 - pos
		p87 - pos
		p88 - pos
		p89 - pos
		o90 - obstacle
		p90 - pos
		p91 - pos
		o92 - obstacle
		p92 - pos
		p93 - pos
		p94 - pos
		p95 - pos
		o96 - obstacle
		p96 - pos
		o97 - obstacle
		p97 - pos
		o98 - obstacle
		p98 - pos
		p99 - pos
		p100 - pos
		o101 - obstacle
		p101 - pos
		p102 - pos
		o103 - obstacle
		p103 - pos
		o104 - obstacle
		p104 - pos
		p105 - pos
		p106 - pos
		o107 - obstacle
		p107 - pos
		o108 - obstacle
		p108 - pos
		o109 - obstacle
		p109 - pos
		p110 - pos
		p111 - pos
		o112 - obstacle
		p112 - pos
		p113 - pos
		p114 - pos
		p115 - pos
		o116 - obstacle
		p116 - pos
		o117 - obstacle
		p117 - pos
		o118 - obstacle
		p118 - pos
		o119 - obstacle
		p119 - pos
		o120 - obstacle
		p120 - pos
		o121 - obstacle
		p121 - pos
		o122 - obstacle
		p122 - pos
		p123 - pos
		o124 - obstacle
		p124 - pos
		o125 - obstacle
		p125 - pos
		o126 - obstacle
		p126 - pos
		p127 - pos
		p128 - pos
		o129 - obstacle
		p129 - pos
		o130 - obstacle
		p130 - pos
		o131 - obstacle
		p131 - pos
		o132 - obstacle
		p132 - pos
		o133 - obstacle
		p133 - pos
		o134 - obstacle
		p134 - pos
		o135 - obstacle
		p135 - pos
		o136 - obstacle
		p136 - pos
		o137 - obstacle
		p137 - pos
		o138 - obstacle
		p138 - pos
		o139 - obstacle
		p139 - pos
		o140 - obstacle
		p140 - pos
		o141 - obstacle
		p141 - pos
		o142 - obstacle
		p142 - pos
		o143 - obstacle
		p143 - pos
		o144 - obstacle
    )
    (:init
		(rAt r p13)
		(handempty)
		(dirIsLeft r)
		(oAt o1 p0)
		(upTo p0 p12)
		(leftTo p0 p1)
		(oAt o2 p1)
		(upTo p1 p13)
		(leftTo p1 p2)
		(rightTo p1 p0)
		(oAt o3 p2)
		(upTo p2 p14)
		(leftTo p2 p3)
		(rightTo p2 p1)
		(oAt o4 p3)
		(upTo p3 p15)
		(leftTo p3 p4)
		(rightTo p3 p2)
		(oAt o5 p4)
		(upTo p4 p16)
		(leftTo p4 p5)
		(rightTo p4 p3)
		(oAt o6 p5)
		(upTo p5 p17)
		(leftTo p5 p6)
		(rightTo p5 p4)
		(oAt o7 p6)
		(upTo p6 p18)
		(leftTo p6 p7)
		(rightTo p6 p5)
		(oAt o8 p7)
		(upTo p7 p19)
		(leftTo p7 p8)
		(rightTo p7 p6)
		(oAt o9 p8)
		(upTo p8 p20)
		(leftTo p8 p9)
		(rightTo p8 p7)
		(oAt o10 p9)
		(upTo p9 p21)
		(leftTo p9 p10)
		(rightTo p9 p8)
		(oAt o11 p10)
		(upTo p10 p22)
		(leftTo p10 p11)
		(rightTo p10 p9)
		(oAt o12 p11)
		(upTo p11 p23)
		(rightTo p11 p10)
		(oAt o13 p12)
		(upTo p12 p24)
		(downTo p12 p0)
		(leftTo p12 p13)
		(posEmpty p13)
		(upTo p13 p25)
		(downTo p13 p1)
		(leftTo p13 p14)
		(rightTo p13 p12)
		(posEmpty p14)
		(upTo p14 p26)
		(downTo p14 p2)
		(leftTo p14 p15)
		(rightTo p14 p13)
		(oAt o16 p15)
		(upTo p15 p27)
		(downTo p15 p3)
		(leftTo p15 p16)
		(rightTo p15 p14)
		(posEmpty p16)
		(upTo p16 p28)
		(downTo p16 p4)
		(leftTo p16 p17)
		(rightTo p16 p15)
		(oAt o18 p17)
		(isLight o18)
		(isMoveable o18)
		(onGround o18)
		(clear o18)
		(upTo p17 p29)
		(downTo p17 p5)
		(leftTo p17 p18)
		(rightTo p17 p16)
		(oAt o19 p18)
		(isHeavy o19)
		(isMoveable o19)
		(onGround o19)
		(clear o19)
		(upTo p18 p30)
		(downTo p18 p6)
		(leftTo p18 p19)
		(rightTo p18 p17)
		(oAt o20 p19)
		(upTo p19 p31)
		(downTo p19 p7)
		(leftTo p19 p20)
		(rightTo p19 p18)
		(posEmpty p20)
		(upTo p20 p32)
		(downTo p20 p8)
		(leftTo p20 p21)
		(rightTo p20 p19)
		(posEmpty p21)
		(upTo p21 p33)
		(downTo p21 p9)
		(leftTo p21 p22)
		(rightTo p21 p20)
		(oAt o23 p22)
		(upTo p22 p34)
		(downTo p22 p10)
		(leftTo p22 p23)
		(rightTo p22 p21)
		(oAt o24 p23)
		(upTo p23 p35)
		(downTo p23 p11)
		(rightTo p23 p22)
		(oAt o25 p24)
		(upTo p24 p36)
		(downTo p24 p12)
		(leftTo p24 p25)
		(oAt o26 p25)
		(isLight o26)
		(isMoveable o26)
		(onGround o26)
		(clear o26)
		(upTo p25 p37)
		(downTo p25 p13)
		(leftTo p25 p26)
		(rightTo p25 p24)
		(posEmpty p26)
		(upTo p26 p38)
		(downTo p26 p14)
		(leftTo p26 p27)
		(rightTo p26 p25)
		(posEmpty p27)
		(upTo p27 p39)
		(downTo p27 p15)
		(leftTo p27 p28)
		(rightTo p27 p26)
		(oAt o29 p28)
		(upTo p28 p40)
		(downTo p28 p16)
		(leftTo p28 p29)
		(rightTo p28 p27)
		(posEmpty p29)
		(upTo p29 p41)
		(downTo p29 p17)
		(leftTo p29 p30)
		(rightTo p29 p28)
		(posEmpty p30)
		(upTo p30 p42)
		(downTo p30 p18)
		(leftTo p30 p31)
		(rightTo p30 p29)
		(posEmpty p31)
		(upTo p31 p43)
		(downTo p31 p19)
		(leftTo p31 p32)
		(rightTo p31 p30)
		(posEmpty p32)
		(upTo p32 p44)
		(downTo p32 p20)
		(leftTo p32 p33)
		(rightTo p32 p31)
		(posEmpty p33)
		(upTo p33 p45)
		(downTo p33 p21)
		(leftTo p33 p34)
		(rightTo p33 p32)
		(posEmpty p34)
		(upTo p34 p46)
		(downTo p34 p22)
		(leftTo p34 p35)
		(rightTo p34 p33)
		(oAt o36 p35)
		(upTo p35 p47)
		(downTo p35 p23)
		(rightTo p35 p34)
		(oAt o37 p36)
		(upTo p36 p48)
		(downTo p36 p24)
		(leftTo p36 p37)
		(posEmpty p37)
		(upTo p37 p49)
		(downTo p37 p25)
		(leftTo p37 p38)
		(rightTo p37 p36)
		(posEmpty p38)
		(upTo p38 p50)
		(downTo p38 p26)
		(leftTo p38 p39)
		(rightTo p38 p37)
		(oAt o40 p39)
		(upTo p39 p51)
		(downTo p39 p27)
		(leftTo p39 p40)
		(rightTo p39 p38)
		(posEmpty p40)
		(upTo p40 p52)
		(downTo p40 p28)
		(leftTo p40 p41)
		(rightTo p40 p39)
		(oAt o42 p41)
		(isHeavy o42)
		(isMoveable o42)
		(onGround o42)
		(clear o42)
		(upTo p41 p53)
		(downTo p41 p29)
		(leftTo p41 p42)
		(rightTo p41 p40)
		(oAt o43 p42)
		(upTo p42 p54)
		(downTo p42 p30)
		(leftTo p42 p43)
		(rightTo p42 p41)
		(oAt o44 p43)
		(isHeavy o44)
		(isMoveable o44)
		(onGround o44)
		(clear o44)
		(upTo p43 p55)
		(downTo p43 p31)
		(leftTo p43 p44)
		(rightTo p43 p42)
		(posEmpty p44)
		(upTo p44 p56)
		(downTo p44 p32)
		(leftTo p44 p45)
		(rightTo p44 p43)
		(oAt o46 p45)
		(upTo p45 p57)
		(downTo p45 p33)
		(leftTo p45 p46)
		(rightTo p45 p44)
		(posEmpty p46)
		(upTo p46 p58)
		(downTo p46 p34)
		(leftTo p46 p47)
		(rightTo p46 p45)
		(oAt o48 p47)
		(upTo p47 p59)
		(downTo p47 p35)
		(rightTo p47 p46)
		(oAt o49 p48)
		(upTo p48 p60)
		(downTo p48 p36)
		(leftTo p48 p49)
		(oAt o50 p49)
		(upTo p49 p61)
		(downTo p49 p37)
		(leftTo p49 p50)
		(rightTo p49 p48)
		(posEmpty p50)
		(upTo p50 p62)
		(downTo p50 p38)
		(leftTo p50 p51)
		(rightTo p50 p49)
		(posEmpty p51)
		(upTo p51 p63)
		(downTo p51 p39)
		(leftTo p51 p52)
		(rightTo p51 p50)
		(posEmpty p52)
		(upTo p52 p64)
		(downTo p52 p40)
		(leftTo p52 p53)
		(rightTo p52 p51)
		(oAt o54 p53)
		(upTo p53 p65)
		(downTo p53 p41)
		(leftTo p53 p54)
		(rightTo p53 p52)
		(posEmpty p54)
		(upTo p54 p66)
		(downTo p54 p42)
		(leftTo p54 p55)
		(rightTo p54 p53)
		(oAt o56 p55)
		(upTo p55 p67)
		(downTo p55 p43)
		(leftTo p55 p56)
		(rightTo p55 p54)
		(oAt o57 p56)
		(isHeavy o57)
		(isMoveable o57)
		(onGround o57)
		(clear o57)
		(upTo p56 p68)
		(downTo p56 p44)
		(leftTo p56 p57)
		(rightTo p56 p55)
		(oAt o58 p57)
		(isHeavy o58)
		(isMoveable o58)
		(onGround o58)
		(clear o58)
		(upTo p57 p69)
		(downTo p57 p45)
		(leftTo p57 p58)
		(rightTo p57 p56)
		(oAt o59 p58)
		(upTo p58 p70)
		(downTo p58 p46)
		(leftTo p58 p59)
		(rightTo p58 p57)
		(oAt o60 p59)
		(upTo p59 p71)
		(downTo p59 p47)
		(rightTo p59 p58)
		(oAt o61 p60)
		(upTo p60 p72)
		(downTo p60 p48)
		(leftTo p60 p61)
		(posEmpty p61)
		(upTo p61 p73)
		(downTo p61 p49)
		(leftTo p61 p62)
		(rightTo p61 p60)
		(oAt o63 p62)
		(isLight o63)
		(isMoveable o63)
		(onGround o63)
		(clear o63)
		(upTo p62 p74)
		(downTo p62 p50)
		(leftTo p62 p63)
		(rightTo p62 p61)
		(oAt o64 p63)
		(upTo p63 p75)
		(downTo p63 p51)
		(leftTo p63 p64)
		(rightTo p63 p62)
		(oAt o65 p64)
		(isLight o65)
		(isMoveable o65)
		(onGround o65)
		(clear o65)
		(upTo p64 p76)
		(downTo p64 p52)
		(leftTo p64 p65)
		(rightTo p64 p63)
		(oAt o66 p65)
		(isLight o66)
		(isMoveable o66)
		(onGround o66)
		(clear o66)
		(upTo p65 p77)
		(downTo p65 p53)
		(leftTo p65 p66)
		(rightTo p65 p64)
		(oAt o67 p66)
		(upTo p66 p78)
		(downTo p66 p54)
		(leftTo p66 p67)
		(rightTo p66 p65)
		(posEmpty p67)
		(upTo p67 p79)
		(downTo p67 p55)
		(leftTo p67 p68)
		(rightTo p67 p66)
		(posEmpty p68)
		(upTo p68 p80)
		(downTo p68 p56)
		(leftTo p68 p69)
		(rightTo p68 p67)
		(oAt o70 p69)
		(isLight o70)
		(isMoveable o70)
		(onGround o70)
		(clear o70)
		(upTo p69 p81)
		(downTo p69 p57)
		(leftTo p69 p70)
		(rightTo p69 p68)
		(oAt o71 p70)
		(upTo p70 p82)
		(downTo p70 p58)
		(leftTo p70 p71)
		(rightTo p70 p69)
		(oAt o72 p71)
		(upTo p71 p83)
		(downTo p71 p59)
		(rightTo p71 p70)
		(oAt o73 p72)
		(upTo p72 p84)
		(downTo p72 p60)
		(leftTo p72 p73)
		(oAt o74 p73)
		(isLight o74)
		(isMoveable o74)
		(onGround o74)
		(clear o74)
		(upTo p73 p85)
		(downTo p73 p61)
		(leftTo p73 p74)
		(rightTo p73 p72)
		(oAt o75 p74)
		(isHeavy o75)
		(isMoveable o75)
		(onGround o75)
		(clear o75)
		(upTo p74 p86)
		(downTo p74 p62)
		(leftTo p74 p75)
		(rightTo p74 p73)
		(oAt o76 p75)
		(isLight o76)
		(isMoveable o76)
		(onGround o76)
		(clear o76)
		(upTo p75 p87)
		(downTo p75 p63)
		(leftTo p75 p76)
		(rightTo p75 p74)
		(oAt o77 p76)
		(upTo p76 p88)
		(downTo p76 p64)
		(leftTo p76 p77)
		(rightTo p76 p75)
		(oAt o78 p77)
		(upTo p77 p89)
		(downTo p77 p65)
		(leftTo p77 p78)
		(rightTo p77 p76)
		(oAt o79 p78)
		(upTo p78 p90)
		(downTo p78 p66)
		(leftTo p78 p79)
		(rightTo p78 p77)
		(oAt o80 p79)
		(upTo p79 p91)
		(downTo p79 p67)
		(leftTo p79 p80)
		(rightTo p79 p78)
		(posEmpty p80)
		(upTo p80 p92)
		(downTo p80 p68)
		(leftTo p80 p81)
		(rightTo p80 p79)
		(posEmpty p81)
		(upTo p81 p93)
		(downTo p81 p69)
		(leftTo p81 p82)
		(rightTo p81 p80)
		(oAt o83 p82)
		(upTo p82 p94)
		(downTo p82 p70)
		(leftTo p82 p83)
		(rightTo p82 p81)
		(oAt o84 p83)
		(upTo p83 p95)
		(downTo p83 p71)
		(rightTo p83 p82)
		(oAt o85 p84)
		(upTo p84 p96)
		(downTo p84 p72)
		(leftTo p84 p85)
		(oAt o86 p85)
		(upTo p85 p97)
		(downTo p85 p73)
		(leftTo p85 p86)
		(rightTo p85 p84)
		(posEmpty p86)
		(upTo p86 p98)
		(downTo p86 p74)
		(leftTo p86 p87)
		(rightTo p86 p85)
		(posEmpty p87)
		(upTo p87 p99)
		(downTo p87 p75)
		(leftTo p87 p88)
		(rightTo p87 p86)
		(posEmpty p88)
		(upTo p88 p100)
		(downTo p88 p76)
		(leftTo p88 p89)
		(rightTo p88 p87)
		(oAt o90 p89)
		(isLight o90)
		(isMoveable o90)
		(onGround o90)
		(clear o90)
		(upTo p89 p101)
		(downTo p89 p77)
		(leftTo p89 p90)
		(rightTo p89 p88)
		(posEmpty p90)
		(upTo p90 p102)
		(downTo p90 p78)
		(leftTo p90 p91)
		(rightTo p90 p89)
		(oAt o92 p91)
		(isLight o92)
		(isMoveable o92)
		(onGround o92)
		(clear o92)
		(upTo p91 p103)
		(downTo p91 p79)
		(leftTo p91 p92)
		(rightTo p91 p90)
		(posEmpty p92)
		(upTo p92 p104)
		(downTo p92 p80)
		(leftTo p92 p93)
		(rightTo p92 p91)
		(posEmpty p93)
		(upTo p93 p105)
		(downTo p93 p81)
		(leftTo p93 p94)
		(rightTo p93 p92)
		(posEmpty p94)
		(upTo p94 p106)
		(downTo p94 p82)
		(leftTo p94 p95)
		(rightTo p94 p93)
		(oAt o96 p95)
		(upTo p95 p107)
		(downTo p95 p83)
		(rightTo p95 p94)
		(oAt o97 p96)
		(upTo p96 p108)
		(downTo p96 p84)
		(leftTo p96 p97)
		(oAt o98 p97)
		(upTo p97 p109)
		(downTo p97 p85)
		(leftTo p97 p98)
		(rightTo p97 p96)
		(posEmpty p98)
		(upTo p98 p110)
		(downTo p98 p86)
		(leftTo p98 p99)
		(rightTo p98 p97)
		(posEmpty p99)
		(upTo p99 p111)
		(downTo p99 p87)
		(leftTo p99 p100)
		(rightTo p99 p98)
		(oAt o101 p100)
		(isLight o101)
		(isMoveable o101)
		(onGround o101)
		(clear o101)
		(upTo p100 p112)
		(downTo p100 p88)
		(leftTo p100 p101)
		(rightTo p100 p99)
		(posEmpty p101)
		(upTo p101 p113)
		(downTo p101 p89)
		(leftTo p101 p102)
		(rightTo p101 p100)
		(oAt o103 p102)
		(upTo p102 p114)
		(downTo p102 p90)
		(leftTo p102 p103)
		(rightTo p102 p101)
		(oAt o104 p103)
		(isLight o104)
		(isMoveable o104)
		(onGround o104)
		(clear o104)
		(upTo p103 p115)
		(downTo p103 p91)
		(leftTo p103 p104)
		(rightTo p103 p102)
		(posEmpty p104)
		(upTo p104 p116)
		(downTo p104 p92)
		(leftTo p104 p105)
		(rightTo p104 p103)
		(posEmpty p105)
		(upTo p105 p117)
		(downTo p105 p93)
		(leftTo p105 p106)
		(rightTo p105 p104)
		(oAt o107 p106)
		(isLight o107)
		(isMoveable o107)
		(onGround o107)
		(clear o107)
		(upTo p106 p118)
		(downTo p106 p94)
		(leftTo p106 p107)
		(rightTo p106 p105)
		(oAt o108 p107)
		(upTo p107 p119)
		(downTo p107 p95)
		(rightTo p107 p106)
		(oAt o109 p108)
		(upTo p108 p120)
		(downTo p108 p96)
		(leftTo p108 p109)
		(posEmpty p109)
		(upTo p109 p121)
		(downTo p109 p97)
		(leftTo p109 p110)
		(rightTo p109 p108)
		(posEmpty p110)
		(upTo p110 p122)
		(downTo p110 p98)
		(leftTo p110 p111)
		(rightTo p110 p109)
		(oAt o112 p111)
		(isHeavy o112)
		(isMoveable o112)
		(onGround o112)
		(clear o112)
		(upTo p111 p123)
		(downTo p111 p99)
		(leftTo p111 p112)
		(rightTo p111 p110)
		(posEmpty p112)
		(upTo p112 p124)
		(downTo p112 p100)
		(leftTo p112 p113)
		(rightTo p112 p111)
		(posEmpty p113)
		(upTo p113 p125)
		(downTo p113 p101)
		(leftTo p113 p114)
		(rightTo p113 p112)
		(posEmpty p114)
		(upTo p114 p126)
		(downTo p114 p102)
		(leftTo p114 p115)
		(rightTo p114 p113)
		(oAt o116 p115)
		(upTo p115 p127)
		(downTo p115 p103)
		(leftTo p115 p116)
		(rightTo p115 p114)
		(oAt o117 p116)
		(upTo p116 p128)
		(downTo p116 p104)
		(leftTo p116 p117)
		(rightTo p116 p115)
		(oAt o118 p117)
		(isHeavy o118)
		(isMoveable o118)
		(onGround o118)
		(clear o118)
		(upTo p117 p129)
		(downTo p117 p105)
		(leftTo p117 p118)
		(rightTo p117 p116)
		(oAt o119 p118)
		(isLight o119)
		(isMoveable o119)
		(onGround o119)
		(clear o119)
		(upTo p118 p130)
		(downTo p118 p106)
		(leftTo p118 p119)
		(rightTo p118 p117)
		(oAt o120 p119)
		(upTo p119 p131)
		(downTo p119 p107)
		(rightTo p119 p118)
		(oAt o121 p120)
		(upTo p120 p132)
		(downTo p120 p108)
		(leftTo p120 p121)
		(oAt o122 p121)
		(upTo p121 p133)
		(downTo p121 p109)
		(leftTo p121 p122)
		(rightTo p121 p120)
		(posEmpty p122)
		(upTo p122 p134)
		(downTo p122 p110)
		(leftTo p122 p123)
		(rightTo p122 p121)
		(oAt o124 p123)
		(isHeavy o124)
		(isMoveable o124)
		(onGround o124)
		(clear o124)
		(upTo p123 p135)
		(downTo p123 p111)
		(leftTo p123 p124)
		(rightTo p123 p122)
		(oAt o125 p124)
		(isHeavy o125)
		(isMoveable o125)
		(onGround o125)
		(clear o125)
		(upTo p124 p136)
		(downTo p124 p112)
		(leftTo p124 p125)
		(rightTo p124 p123)
		(oAt o126 p125)
		(isLight o126)
		(isMoveable o126)
		(onGround o126)
		(clear o126)
		(upTo p125 p137)
		(downTo p125 p113)
		(leftTo p125 p126)
		(rightTo p125 p124)
		(posEmpty p126)
		(upTo p126 p138)
		(downTo p126 p114)
		(leftTo p126 p127)
		(rightTo p126 p125)
		(posEmpty p127)
		(upTo p127 p139)
		(downTo p127 p115)
		(leftTo p127 p128)
		(rightTo p127 p126)
		(oAt o129 p128)
		(upTo p128 p140)
		(downTo p128 p116)
		(leftTo p128 p129)
		(rightTo p128 p127)
		(oAt o130 p129)
		(isLight o130)
		(isMoveable o130)
		(onGround o130)
		(clear o130)
		(upTo p129 p141)
		(downTo p129 p117)
		(leftTo p129 p130)
		(rightTo p129 p128)
		(oAt o131 p130)
		(isHeavy o131)
		(isMoveable o131)
		(onGround o131)
		(clear o131)
		(upTo p130 p142)
		(downTo p130 p118)
		(leftTo p130 p131)
		(rightTo p130 p129)
		(oAt o132 p131)
		(upTo p131 p143)
		(downTo p131 p119)
		(rightTo p131 p130)
		(oAt o133 p132)
		(downTo p132 p120)
		(leftTo p132 p133)
		(oAt o134 p133)
		(downTo p133 p121)
		(leftTo p133 p134)
		(rightTo p133 p132)
		(oAt o135 p134)
		(downTo p134 p122)
		(leftTo p134 p135)
		(rightTo p134 p133)
		(oAt o136 p135)
		(downTo p135 p123)
		(leftTo p135 p136)
		(rightTo p135 p134)
		(oAt o137 p136)
		(downTo p136 p124)
		(leftTo p136 p137)
		(rightTo p136 p135)
		(oAt o138 p137)
		(downTo p137 p125)
		(leftTo p137 p138)
		(rightTo p137 p136)
		(oAt o139 p138)
		(downTo p138 p126)
		(leftTo p138 p139)
		(rightTo p138 p137)
		(oAt o140 p139)
		(downTo p139 p127)
		(leftTo p139 p140)
		(rightTo p139 p138)
		(oAt o141 p140)
		(downTo p140 p128)
		(leftTo p140 p141)
		(rightTo p140 p139)
		(oAt o142 p141)
		(downTo p141 p129)
		(leftTo p141 p142)
		(rightTo p141 p140)
		(oAt o143 p142)
		(downTo p142 p130)
		(leftTo p142 p143)
		(rightTo p142 p141)
		(oAt o144 p143)
		(downTo p143 p131)
		(rightTo p143 p142)
    )
    (:goal
		(rAt r p94)
    )
    )