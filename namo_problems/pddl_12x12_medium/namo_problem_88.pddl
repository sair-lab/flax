(define (problem namo_problem)
    (:domain namo)
    (:objects
		r - robot
		p0 - pos
		o1 - object
		p1 - pos
		o2 - object
		p2 - pos
		o3 - object
		p3 - pos
		o4 - object
		p4 - pos
		o5 - object
		p5 - pos
		o6 - object
		p6 - pos
		o7 - object
		p7 - pos
		o8 - object
		p8 - pos
		o9 - object
		p9 - pos
		o10 - object
		p10 - pos
		o11 - object
		p11 - pos
		o12 - object
		p12 - pos
		o13 - object
		p13 - pos
		o14 - object
		p14 - pos
		p15 - pos
		p16 - pos
		p17 - pos
		p18 - pos
		p19 - pos
		o20 - object
		p20 - pos
		o21 - object
		p21 - pos
		p22 - pos
		o23 - object
		p23 - pos
		o24 - object
		p24 - pos
		o25 - object
		p25 - pos
		p26 - pos
		o27 - object
		p27 - pos
		p28 - pos
		o29 - object
		p29 - pos
		p30 - pos
		o31 - object
		p31 - pos
		o32 - object
		p32 - pos
		o33 - object
		p33 - pos
		o34 - object
		p34 - pos
		o35 - object
		p35 - pos
		o36 - object
		p36 - pos
		o37 - object
		p37 - pos
		o38 - object
		p38 - pos
		o39 - object
		p39 - pos
		o40 - object
		p40 - pos
		o41 - object
		p41 - pos
		p42 - pos
		p43 - pos
		o44 - object
		p44 - pos
		o45 - object
		p45 - pos
		o46 - object
		p46 - pos
		p47 - pos
		o48 - object
		p48 - pos
		o49 - object
		p49 - pos
		o50 - object
		p50 - pos
		p51 - pos
		o52 - object
		p52 - pos
		p53 - pos
		o54 - object
		p54 - pos
		p55 - pos
		o56 - object
		p56 - pos
		p57 - pos
		o58 - object
		p58 - pos
		p59 - pos
		o60 - object
		p60 - pos
		o61 - object
		p61 - pos
		o62 - object
		p62 - pos
		p63 - pos
		o64 - object
		p64 - pos
		o65 - object
		p65 - pos
		p66 - pos
		o67 - object
		p67 - pos
		o68 - object
		p68 - pos
		o69 - object
		p69 - pos
		o70 - object
		p70 - pos
		p71 - pos
		o72 - object
		p72 - pos
		o73 - object
		p73 - pos
		p74 - pos
		p75 - pos
		p76 - pos
		p77 - pos
		p78 - pos
		o79 - object
		p79 - pos
		p80 - pos
		o81 - object
		p81 - pos
		o82 - object
		p82 - pos
		p83 - pos
		o84 - object
		p84 - pos
		o85 - object
		p85 - pos
		p86 - pos
		p87 - pos
		o88 - object
		p88 - pos
		o89 - object
		p89 - pos
		o90 - object
		p90 - pos
		o91 - object
		p91 - pos
		p92 - pos
		p93 - pos
		p94 - pos
		o95 - object
		p95 - pos
		o96 - object
		p96 - pos
		o97 - object
		p97 - pos
		p98 - pos
		p99 - pos
		p100 - pos
		p101 - pos
		p102 - pos
		p103 - pos
		o104 - object
		p104 - pos
		p105 - pos
		o106 - object
		p106 - pos
		o107 - object
		p107 - pos
		o108 - object
		p108 - pos
		o109 - object
		p109 - pos
		p110 - pos
		o111 - object
		p111 - pos
		o112 - object
		p112 - pos
		p113 - pos
		o114 - object
		p114 - pos
		p115 - pos
		p116 - pos
		o117 - object
		p117 - pos
		p118 - pos
		p119 - pos
		o120 - object
		p120 - pos
		o121 - object
		p121 - pos
		o122 - object
		p122 - pos
		p123 - pos
		p124 - pos
		p125 - pos
		p126 - pos
		o127 - object
		p127 - pos
		p128 - pos
		o129 - object
		p129 - pos
		p130 - pos
		p131 - pos
		o132 - object
		p132 - pos
		o133 - object
		p133 - pos
		o134 - object
		p134 - pos
		o135 - object
		p135 - pos
		o136 - object
		p136 - pos
		o137 - object
		p137 - pos
		o138 - object
		p138 - pos
		o139 - object
		p139 - pos
		o140 - object
		p140 - pos
		o141 - object
		p141 - pos
		o142 - object
		p142 - pos
		o143 - object
		p143 - pos
		o144 - object
    )
    (:init
		(rAt r p73)
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
		(oAt o14 p13)
		(isLight o14)
		(isMoveable o14)
		(onGround o14)
		(clear o14)
		(upTo p13 p25)
		(downTo p13 p1)
		(leftTo p13 p14)
		(rightTo p13 p12)
		(posEmpty p14)
		(upTo p14 p26)
		(downTo p14 p2)
		(leftTo p14 p15)
		(rightTo p14 p13)
		(posEmpty p15)
		(upTo p15 p27)
		(downTo p15 p3)
		(leftTo p15 p16)
		(rightTo p15 p14)
		(posEmpty p16)
		(upTo p16 p28)
		(downTo p16 p4)
		(leftTo p16 p17)
		(rightTo p16 p15)
		(posEmpty p17)
		(upTo p17 p29)
		(downTo p17 p5)
		(leftTo p17 p18)
		(rightTo p17 p16)
		(posEmpty p18)
		(upTo p18 p30)
		(downTo p18 p6)
		(leftTo p18 p19)
		(rightTo p18 p17)
		(oAt o20 p19)
		(upTo p19 p31)
		(downTo p19 p7)
		(leftTo p19 p20)
		(rightTo p19 p18)
		(oAt o21 p20)
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
		(posEmpty p25)
		(upTo p25 p37)
		(downTo p25 p13)
		(leftTo p25 p26)
		(rightTo p25 p24)
		(oAt o27 p26)
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
		(isLight o29)
		(isMoveable o29)
		(onGround o29)
		(clear o29)
		(upTo p28 p40)
		(downTo p28 p16)
		(leftTo p28 p29)
		(rightTo p28 p27)
		(posEmpty p29)
		(upTo p29 p41)
		(downTo p29 p17)
		(leftTo p29 p30)
		(rightTo p29 p28)
		(oAt o31 p30)
		(isHeavy o31)
		(isMoveable o31)
		(onGround o31)
		(clear o31)
		(upTo p30 p42)
		(downTo p30 p18)
		(leftTo p30 p31)
		(rightTo p30 p29)
		(oAt o32 p31)
		(isLight o32)
		(isMoveable o32)
		(onGround o32)
		(clear o32)
		(upTo p31 p43)
		(downTo p31 p19)
		(leftTo p31 p32)
		(rightTo p31 p30)
		(oAt o33 p32)
		(upTo p32 p44)
		(downTo p32 p20)
		(leftTo p32 p33)
		(rightTo p32 p31)
		(oAt o34 p33)
		(isLight o34)
		(isMoveable o34)
		(onGround o34)
		(clear o34)
		(upTo p33 p45)
		(downTo p33 p21)
		(leftTo p33 p34)
		(rightTo p33 p32)
		(oAt o35 p34)
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
		(oAt o38 p37)
		(isLight o38)
		(isMoveable o38)
		(onGround o38)
		(clear o38)
		(upTo p37 p49)
		(downTo p37 p25)
		(leftTo p37 p38)
		(rightTo p37 p36)
		(oAt o39 p38)
		(isLight o39)
		(isMoveable o39)
		(onGround o39)
		(clear o39)
		(upTo p38 p50)
		(downTo p38 p26)
		(leftTo p38 p39)
		(rightTo p38 p37)
		(oAt o40 p39)
		(isLight o40)
		(isMoveable o40)
		(onGround o40)
		(clear o40)
		(upTo p39 p51)
		(downTo p39 p27)
		(leftTo p39 p40)
		(rightTo p39 p38)
		(oAt o41 p40)
		(isHeavy o41)
		(isMoveable o41)
		(onGround o41)
		(clear o41)
		(upTo p40 p52)
		(downTo p40 p28)
		(leftTo p40 p41)
		(rightTo p40 p39)
		(posEmpty p41)
		(upTo p41 p53)
		(downTo p41 p29)
		(leftTo p41 p42)
		(rightTo p41 p40)
		(posEmpty p42)
		(upTo p42 p54)
		(downTo p42 p30)
		(leftTo p42 p43)
		(rightTo p42 p41)
		(oAt o44 p43)
		(isLight o44)
		(isMoveable o44)
		(onGround o44)
		(clear o44)
		(upTo p43 p55)
		(downTo p43 p31)
		(leftTo p43 p44)
		(rightTo p43 p42)
		(oAt o45 p44)
		(isLight o45)
		(isMoveable o45)
		(onGround o45)
		(clear o45)
		(upTo p44 p56)
		(downTo p44 p32)
		(leftTo p44 p45)
		(rightTo p44 p43)
		(oAt o46 p45)
		(isHeavy o46)
		(isMoveable o46)
		(onGround o46)
		(clear o46)
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
		(isLight o50)
		(isMoveable o50)
		(onGround o50)
		(clear o50)
		(upTo p49 p61)
		(downTo p49 p37)
		(leftTo p49 p50)
		(rightTo p49 p48)
		(posEmpty p50)
		(upTo p50 p62)
		(downTo p50 p38)
		(leftTo p50 p51)
		(rightTo p50 p49)
		(oAt o52 p51)
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
		(isHeavy o54)
		(isMoveable o54)
		(onGround o54)
		(clear o54)
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
		(isHeavy o56)
		(isMoveable o56)
		(onGround o56)
		(clear o56)
		(upTo p55 p67)
		(downTo p55 p43)
		(leftTo p55 p56)
		(rightTo p55 p54)
		(posEmpty p56)
		(upTo p56 p68)
		(downTo p56 p44)
		(leftTo p56 p57)
		(rightTo p56 p55)
		(oAt o58 p57)
		(isLight o58)
		(isMoveable o58)
		(onGround o58)
		(clear o58)
		(upTo p57 p69)
		(downTo p57 p45)
		(leftTo p57 p58)
		(rightTo p57 p56)
		(posEmpty p58)
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
		(oAt o62 p61)
		(isLight o62)
		(isMoveable o62)
		(onGround o62)
		(clear o62)
		(upTo p61 p73)
		(downTo p61 p49)
		(leftTo p61 p62)
		(rightTo p61 p60)
		(posEmpty p62)
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
		(posEmpty p65)
		(upTo p65 p77)
		(downTo p65 p53)
		(leftTo p65 p66)
		(rightTo p65 p64)
		(oAt o67 p66)
		(isHeavy o67)
		(isMoveable o67)
		(onGround o67)
		(clear o67)
		(upTo p66 p78)
		(downTo p66 p54)
		(leftTo p66 p67)
		(rightTo p66 p65)
		(oAt o68 p67)
		(isLight o68)
		(isMoveable o68)
		(onGround o68)
		(clear o68)
		(upTo p67 p79)
		(downTo p67 p55)
		(leftTo p67 p68)
		(rightTo p67 p66)
		(oAt o69 p68)
		(upTo p68 p80)
		(downTo p68 p56)
		(leftTo p68 p69)
		(rightTo p68 p67)
		(oAt o70 p69)
		(upTo p69 p81)
		(downTo p69 p57)
		(leftTo p69 p70)
		(rightTo p69 p68)
		(posEmpty p70)
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
		(posEmpty p73)
		(upTo p73 p85)
		(downTo p73 p61)
		(leftTo p73 p74)
		(rightTo p73 p72)
		(posEmpty p74)
		(upTo p74 p86)
		(downTo p74 p62)
		(leftTo p74 p75)
		(rightTo p74 p73)
		(posEmpty p75)
		(upTo p75 p87)
		(downTo p75 p63)
		(leftTo p75 p76)
		(rightTo p75 p74)
		(posEmpty p76)
		(upTo p76 p88)
		(downTo p76 p64)
		(leftTo p76 p77)
		(rightTo p76 p75)
		(posEmpty p77)
		(upTo p77 p89)
		(downTo p77 p65)
		(leftTo p77 p78)
		(rightTo p77 p76)
		(oAt o79 p78)
		(isLight o79)
		(isMoveable o79)
		(onGround o79)
		(clear o79)
		(upTo p78 p90)
		(downTo p78 p66)
		(leftTo p78 p79)
		(rightTo p78 p77)
		(posEmpty p79)
		(upTo p79 p91)
		(downTo p79 p67)
		(leftTo p79 p80)
		(rightTo p79 p78)
		(oAt o81 p80)
		(upTo p80 p92)
		(downTo p80 p68)
		(leftTo p80 p81)
		(rightTo p80 p79)
		(oAt o82 p81)
		(isLight o82)
		(isMoveable o82)
		(onGround o82)
		(clear o82)
		(upTo p81 p93)
		(downTo p81 p69)
		(leftTo p81 p82)
		(rightTo p81 p80)
		(posEmpty p82)
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
		(posEmpty p85)
		(upTo p85 p97)
		(downTo p85 p73)
		(leftTo p85 p86)
		(rightTo p85 p84)
		(posEmpty p86)
		(upTo p86 p98)
		(downTo p86 p74)
		(leftTo p86 p87)
		(rightTo p86 p85)
		(oAt o88 p87)
		(isLight o88)
		(isMoveable o88)
		(onGround o88)
		(clear o88)
		(upTo p87 p99)
		(downTo p87 p75)
		(leftTo p87 p88)
		(rightTo p87 p86)
		(oAt o89 p88)
		(upTo p88 p100)
		(downTo p88 p76)
		(leftTo p88 p89)
		(rightTo p88 p87)
		(oAt o90 p89)
		(isHeavy o90)
		(isMoveable o90)
		(onGround o90)
		(clear o90)
		(upTo p89 p101)
		(downTo p89 p77)
		(leftTo p89 p90)
		(rightTo p89 p88)
		(oAt o91 p90)
		(isLight o91)
		(isMoveable o91)
		(onGround o91)
		(clear o91)
		(upTo p90 p102)
		(downTo p90 p78)
		(leftTo p90 p91)
		(rightTo p90 p89)
		(posEmpty p91)
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
		(oAt o95 p94)
		(isLight o95)
		(isMoveable o95)
		(onGround o95)
		(clear o95)
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
		(posEmpty p97)
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
		(posEmpty p100)
		(upTo p100 p112)
		(downTo p100 p88)
		(leftTo p100 p101)
		(rightTo p100 p99)
		(posEmpty p101)
		(upTo p101 p113)
		(downTo p101 p89)
		(leftTo p101 p102)
		(rightTo p101 p100)
		(posEmpty p102)
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
		(oAt o106 p105)
		(isLight o106)
		(isMoveable o106)
		(onGround o106)
		(clear o106)
		(upTo p105 p117)
		(downTo p105 p93)
		(leftTo p105 p106)
		(rightTo p105 p104)
		(oAt o107 p106)
		(isHeavy o107)
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
		(oAt o111 p110)
		(isHeavy o111)
		(isMoveable o111)
		(onGround o111)
		(clear o111)
		(upTo p110 p122)
		(downTo p110 p98)
		(leftTo p110 p111)
		(rightTo p110 p109)
		(oAt o112 p111)
		(isLight o112)
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
		(oAt o114 p113)
		(isLight o114)
		(isMoveable o114)
		(onGround o114)
		(clear o114)
		(upTo p113 p125)
		(downTo p113 p101)
		(leftTo p113 p114)
		(rightTo p113 p112)
		(posEmpty p114)
		(upTo p114 p126)
		(downTo p114 p102)
		(leftTo p114 p115)
		(rightTo p114 p113)
		(posEmpty p115)
		(upTo p115 p127)
		(downTo p115 p103)
		(leftTo p115 p116)
		(rightTo p115 p114)
		(oAt o117 p116)
		(upTo p116 p128)
		(downTo p116 p104)
		(leftTo p116 p117)
		(rightTo p116 p115)
		(posEmpty p117)
		(upTo p117 p129)
		(downTo p117 p105)
		(leftTo p117 p118)
		(rightTo p117 p116)
		(posEmpty p118)
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
		(isLight o122)
		(isMoveable o122)
		(onGround o122)
		(clear o122)
		(upTo p121 p133)
		(downTo p121 p109)
		(leftTo p121 p122)
		(rightTo p121 p120)
		(posEmpty p122)
		(upTo p122 p134)
		(downTo p122 p110)
		(leftTo p122 p123)
		(rightTo p122 p121)
		(posEmpty p123)
		(upTo p123 p135)
		(downTo p123 p111)
		(leftTo p123 p124)
		(rightTo p123 p122)
		(posEmpty p124)
		(upTo p124 p136)
		(downTo p124 p112)
		(leftTo p124 p125)
		(rightTo p124 p123)
		(posEmpty p125)
		(upTo p125 p137)
		(downTo p125 p113)
		(leftTo p125 p126)
		(rightTo p125 p124)
		(oAt o127 p126)
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
		(isHeavy o129)
		(isMoveable o129)
		(onGround o129)
		(clear o129)
		(upTo p128 p140)
		(downTo p128 p116)
		(leftTo p128 p129)
		(rightTo p128 p127)
		(posEmpty p129)
		(upTo p129 p141)
		(downTo p129 p117)
		(leftTo p129 p130)
		(rightTo p129 p128)
		(posEmpty p130)
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
		(rAt r p117)
    )
    )