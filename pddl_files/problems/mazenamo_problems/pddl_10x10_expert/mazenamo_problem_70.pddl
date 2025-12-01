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
		p12 - pos
		p13 - pos
		p14 - pos
		p15 - pos
		p16 - pos
		o17 - obstacle
		p17 - pos
		o18 - obstacle
		p18 - pos
		o19 - obstacle
		p19 - pos
		o20 - obstacle
		p20 - pos
		o21 - obstacle
		p21 - pos
		p22 - pos
		p23 - pos
		o24 - obstacle
		p24 - pos
		o25 - obstacle
		p25 - pos
		o26 - obstacle
		p26 - pos
		o27 - obstacle
		p27 - pos
		o28 - obstacle
		p28 - pos
		p29 - pos
		o30 - obstacle
		p30 - pos
		o31 - obstacle
		p31 - pos
		o32 - obstacle
		p32 - pos
		p33 - pos
		o34 - obstacle
		p34 - pos
		o35 - obstacle
		p35 - pos
		o36 - obstacle
		p36 - pos
		p37 - pos
		p38 - pos
		p39 - pos
		o40 - obstacle
		p40 - pos
		o41 - obstacle
		p41 - pos
		p42 - pos
		o43 - obstacle
		p43 - pos
		p44 - pos
		p45 - pos
		p46 - pos
		p47 - pos
		p48 - pos
		o49 - obstacle
		p49 - pos
		o50 - obstacle
		p50 - pos
		o51 - obstacle
		p51 - pos
		p52 - pos
		o53 - obstacle
		p53 - pos
		o54 - obstacle
		p54 - pos
		o55 - obstacle
		p55 - pos
		p56 - pos
		p57 - pos
		o58 - obstacle
		p58 - pos
		o59 - obstacle
		p59 - pos
		o60 - obstacle
		p60 - pos
		o61 - obstacle
		p61 - pos
		o62 - obstacle
		p62 - pos
		p63 - pos
		p64 - pos
		p65 - pos
		o66 - obstacle
		p66 - pos
		p67 - pos
		p68 - pos
		o69 - obstacle
		p69 - pos
		o70 - obstacle
		p70 - pos
		o71 - obstacle
		p71 - pos
		o72 - obstacle
		p72 - pos
		p73 - pos
		o74 - obstacle
		p74 - pos
		o75 - obstacle
		p75 - pos
		o76 - obstacle
		p76 - pos
		p77 - pos
		p78 - pos
		o79 - obstacle
		p79 - pos
		o80 - obstacle
		p80 - pos
		o81 - obstacle
		p81 - pos
		o82 - obstacle
		p82 - pos
		o83 - obstacle
		p83 - pos
		p84 - pos
		p85 - pos
		p86 - pos
		o87 - obstacle
		p87 - pos
		p88 - pos
		o89 - obstacle
		p89 - pos
		o90 - obstacle
		p90 - pos
		o91 - obstacle
		p91 - pos
		o92 - obstacle
		p92 - pos
		o93 - obstacle
		p93 - pos
		o94 - obstacle
		p94 - pos
		o95 - obstacle
		p95 - pos
		o96 - obstacle
		p96 - pos
		o97 - obstacle
		p97 - pos
		o98 - obstacle
		p98 - pos
		o99 - obstacle
		p99 - pos
		o100 - obstacle
    )
    (:init
		(rAt r p67)
		(handempty)
		(dirIsUp r)
		(oAt o1 p0)
		(upTo p0 p10)
		(leftTo p0 p1)
		(oAt o2 p1)
		(upTo p1 p11)
		(leftTo p1 p2)
		(rightTo p1 p0)
		(oAt o3 p2)
		(upTo p2 p12)
		(leftTo p2 p3)
		(rightTo p2 p1)
		(oAt o4 p3)
		(upTo p3 p13)
		(leftTo p3 p4)
		(rightTo p3 p2)
		(oAt o5 p4)
		(upTo p4 p14)
		(leftTo p4 p5)
		(rightTo p4 p3)
		(oAt o6 p5)
		(upTo p5 p15)
		(leftTo p5 p6)
		(rightTo p5 p4)
		(oAt o7 p6)
		(upTo p6 p16)
		(leftTo p6 p7)
		(rightTo p6 p5)
		(oAt o8 p7)
		(upTo p7 p17)
		(leftTo p7 p8)
		(rightTo p7 p6)
		(oAt o9 p8)
		(upTo p8 p18)
		(leftTo p8 p9)
		(rightTo p8 p7)
		(oAt o10 p9)
		(upTo p9 p19)
		(rightTo p9 p8)
		(oAt o11 p10)
		(upTo p10 p20)
		(downTo p10 p0)
		(leftTo p10 p11)
		(posEmpty p11)
		(upTo p11 p21)
		(downTo p11 p1)
		(leftTo p11 p12)
		(rightTo p11 p10)
		(posEmpty p12)
		(upTo p12 p22)
		(downTo p12 p2)
		(leftTo p12 p13)
		(rightTo p12 p11)
		(posEmpty p13)
		(upTo p13 p23)
		(downTo p13 p3)
		(leftTo p13 p14)
		(rightTo p13 p12)
		(posEmpty p14)
		(upTo p14 p24)
		(downTo p14 p4)
		(leftTo p14 p15)
		(rightTo p14 p13)
		(posEmpty p15)
		(upTo p15 p25)
		(downTo p15 p5)
		(leftTo p15 p16)
		(rightTo p15 p14)
		(oAt o17 p16)
		(upTo p16 p26)
		(downTo p16 p6)
		(leftTo p16 p17)
		(rightTo p16 p15)
		(oAt o18 p17)
		(upTo p17 p27)
		(downTo p17 p7)
		(leftTo p17 p18)
		(rightTo p17 p16)
		(oAt o19 p18)
		(isLight o19)
		(isMoveable o19)
		(onGround o19)
		(clear o19)
		(upTo p18 p28)
		(downTo p18 p8)
		(leftTo p18 p19)
		(rightTo p18 p17)
		(oAt o20 p19)
		(upTo p19 p29)
		(downTo p19 p9)
		(rightTo p19 p18)
		(oAt o21 p20)
		(upTo p20 p30)
		(downTo p20 p10)
		(leftTo p20 p21)
		(posEmpty p21)
		(upTo p21 p31)
		(downTo p21 p11)
		(leftTo p21 p22)
		(rightTo p21 p20)
		(posEmpty p22)
		(upTo p22 p32)
		(downTo p22 p12)
		(leftTo p22 p23)
		(rightTo p22 p21)
		(oAt o24 p23)
		(isHeavy o24)
		(isMoveable o24)
		(onGround o24)
		(clear o24)
		(upTo p23 p33)
		(downTo p23 p13)
		(leftTo p23 p24)
		(rightTo p23 p22)
		(oAt o25 p24)
		(isHeavy o25)
		(isMoveable o25)
		(onGround o25)
		(clear o25)
		(upTo p24 p34)
		(downTo p24 p14)
		(leftTo p24 p25)
		(rightTo p24 p23)
		(oAt o26 p25)
		(upTo p25 p35)
		(downTo p25 p15)
		(leftTo p25 p26)
		(rightTo p25 p24)
		(oAt o27 p26)
		(upTo p26 p36)
		(downTo p26 p16)
		(leftTo p26 p27)
		(rightTo p26 p25)
		(oAt o28 p27)
		(isHeavy o28)
		(isMoveable o28)
		(onGround o28)
		(clear o28)
		(upTo p27 p37)
		(downTo p27 p17)
		(leftTo p27 p28)
		(rightTo p27 p26)
		(posEmpty p28)
		(upTo p28 p38)
		(downTo p28 p18)
		(leftTo p28 p29)
		(rightTo p28 p27)
		(oAt o30 p29)
		(upTo p29 p39)
		(downTo p29 p19)
		(rightTo p29 p28)
		(oAt o31 p30)
		(upTo p30 p40)
		(downTo p30 p20)
		(leftTo p30 p31)
		(oAt o32 p31)
		(upTo p31 p41)
		(downTo p31 p21)
		(leftTo p31 p32)
		(rightTo p31 p30)
		(posEmpty p32)
		(upTo p32 p42)
		(downTo p32 p22)
		(leftTo p32 p33)
		(rightTo p32 p31)
		(oAt o34 p33)
		(upTo p33 p43)
		(downTo p33 p23)
		(leftTo p33 p34)
		(rightTo p33 p32)
		(oAt o35 p34)
		(upTo p34 p44)
		(downTo p34 p24)
		(leftTo p34 p35)
		(rightTo p34 p33)
		(oAt o36 p35)
		(isHeavy o36)
		(isMoveable o36)
		(onGround o36)
		(clear o36)
		(upTo p35 p45)
		(downTo p35 p25)
		(leftTo p35 p36)
		(rightTo p35 p34)
		(posEmpty p36)
		(upTo p36 p46)
		(downTo p36 p26)
		(leftTo p36 p37)
		(rightTo p36 p35)
		(posEmpty p37)
		(upTo p37 p47)
		(downTo p37 p27)
		(leftTo p37 p38)
		(rightTo p37 p36)
		(posEmpty p38)
		(upTo p38 p48)
		(downTo p38 p28)
		(leftTo p38 p39)
		(rightTo p38 p37)
		(oAt o40 p39)
		(upTo p39 p49)
		(downTo p39 p29)
		(rightTo p39 p38)
		(oAt o41 p40)
		(upTo p40 p50)
		(downTo p40 p30)
		(leftTo p40 p41)
		(posEmpty p41)
		(upTo p41 p51)
		(downTo p41 p31)
		(leftTo p41 p42)
		(rightTo p41 p40)
		(oAt o43 p42)
		(isLight o43)
		(isMoveable o43)
		(onGround o43)
		(clear o43)
		(upTo p42 p52)
		(downTo p42 p32)
		(leftTo p42 p43)
		(rightTo p42 p41)
		(posEmpty p43)
		(upTo p43 p53)
		(downTo p43 p33)
		(leftTo p43 p44)
		(rightTo p43 p42)
		(posEmpty p44)
		(upTo p44 p54)
		(downTo p44 p34)
		(leftTo p44 p45)
		(rightTo p44 p43)
		(posEmpty p45)
		(upTo p45 p55)
		(downTo p45 p35)
		(leftTo p45 p46)
		(rightTo p45 p44)
		(posEmpty p46)
		(upTo p46 p56)
		(downTo p46 p36)
		(leftTo p46 p47)
		(rightTo p46 p45)
		(posEmpty p47)
		(upTo p47 p57)
		(downTo p47 p37)
		(leftTo p47 p48)
		(rightTo p47 p46)
		(oAt o49 p48)
		(upTo p48 p58)
		(downTo p48 p38)
		(leftTo p48 p49)
		(rightTo p48 p47)
		(oAt o50 p49)
		(upTo p49 p59)
		(downTo p49 p39)
		(rightTo p49 p48)
		(oAt o51 p50)
		(upTo p50 p60)
		(downTo p50 p40)
		(leftTo p50 p51)
		(posEmpty p51)
		(upTo p51 p61)
		(downTo p51 p41)
		(leftTo p51 p52)
		(rightTo p51 p50)
		(oAt o53 p52)
		(isHeavy o53)
		(isMoveable o53)
		(onGround o53)
		(clear o53)
		(upTo p52 p62)
		(downTo p52 p42)
		(leftTo p52 p53)
		(rightTo p52 p51)
		(oAt o54 p53)
		(upTo p53 p63)
		(downTo p53 p43)
		(leftTo p53 p54)
		(rightTo p53 p52)
		(oAt o55 p54)
		(upTo p54 p64)
		(downTo p54 p44)
		(leftTo p54 p55)
		(rightTo p54 p53)
		(posEmpty p55)
		(upTo p55 p65)
		(downTo p55 p45)
		(leftTo p55 p56)
		(rightTo p55 p54)
		(posEmpty p56)
		(upTo p56 p66)
		(downTo p56 p46)
		(leftTo p56 p57)
		(rightTo p56 p55)
		(oAt o58 p57)
		(isLight o58)
		(isMoveable o58)
		(onGround o58)
		(clear o58)
		(upTo p57 p67)
		(downTo p57 p47)
		(leftTo p57 p58)
		(rightTo p57 p56)
		(oAt o59 p58)
		(isLight o59)
		(isMoveable o59)
		(onGround o59)
		(clear o59)
		(upTo p58 p68)
		(downTo p58 p48)
		(leftTo p58 p59)
		(rightTo p58 p57)
		(oAt o60 p59)
		(upTo p59 p69)
		(downTo p59 p49)
		(rightTo p59 p58)
		(oAt o61 p60)
		(upTo p60 p70)
		(downTo p60 p50)
		(leftTo p60 p61)
		(oAt o62 p61)
		(upTo p61 p71)
		(downTo p61 p51)
		(leftTo p61 p62)
		(rightTo p61 p60)
		(posEmpty p62)
		(upTo p62 p72)
		(downTo p62 p52)
		(leftTo p62 p63)
		(rightTo p62 p61)
		(posEmpty p63)
		(upTo p63 p73)
		(downTo p63 p53)
		(leftTo p63 p64)
		(rightTo p63 p62)
		(posEmpty p64)
		(upTo p64 p74)
		(downTo p64 p54)
		(leftTo p64 p65)
		(rightTo p64 p63)
		(oAt o66 p65)
		(upTo p65 p75)
		(downTo p65 p55)
		(leftTo p65 p66)
		(rightTo p65 p64)
		(posEmpty p66)
		(upTo p66 p76)
		(downTo p66 p56)
		(leftTo p66 p67)
		(rightTo p66 p65)
		(posEmpty p67)
		(upTo p67 p77)
		(downTo p67 p57)
		(leftTo p67 p68)
		(rightTo p67 p66)
		(oAt o69 p68)
		(isLight o69)
		(isMoveable o69)
		(onGround o69)
		(clear o69)
		(upTo p68 p78)
		(downTo p68 p58)
		(leftTo p68 p69)
		(rightTo p68 p67)
		(oAt o70 p69)
		(upTo p69 p79)
		(downTo p69 p59)
		(rightTo p69 p68)
		(oAt o71 p70)
		(upTo p70 p80)
		(downTo p70 p60)
		(leftTo p70 p71)
		(oAt o72 p71)
		(isLight o72)
		(isMoveable o72)
		(onGround o72)
		(clear o72)
		(upTo p71 p81)
		(downTo p71 p61)
		(leftTo p71 p72)
		(rightTo p71 p70)
		(posEmpty p72)
		(upTo p72 p82)
		(downTo p72 p62)
		(leftTo p72 p73)
		(rightTo p72 p71)
		(oAt o74 p73)
		(upTo p73 p83)
		(downTo p73 p63)
		(leftTo p73 p74)
		(rightTo p73 p72)
		(oAt o75 p74)
		(isHeavy o75)
		(isMoveable o75)
		(onGround o75)
		(clear o75)
		(upTo p74 p84)
		(downTo p74 p64)
		(leftTo p74 p75)
		(rightTo p74 p73)
		(oAt o76 p75)
		(upTo p75 p85)
		(downTo p75 p65)
		(leftTo p75 p76)
		(rightTo p75 p74)
		(posEmpty p76)
		(upTo p76 p86)
		(downTo p76 p66)
		(leftTo p76 p77)
		(rightTo p76 p75)
		(posEmpty p77)
		(upTo p77 p87)
		(downTo p77 p67)
		(leftTo p77 p78)
		(rightTo p77 p76)
		(oAt o79 p78)
		(isHeavy o79)
		(isMoveable o79)
		(onGround o79)
		(clear o79)
		(upTo p78 p88)
		(downTo p78 p68)
		(leftTo p78 p79)
		(rightTo p78 p77)
		(oAt o80 p79)
		(upTo p79 p89)
		(downTo p79 p69)
		(rightTo p79 p78)
		(oAt o81 p80)
		(upTo p80 p90)
		(downTo p80 p70)
		(leftTo p80 p81)
		(oAt o82 p81)
		(isLight o82)
		(isMoveable o82)
		(onGround o82)
		(clear o82)
		(upTo p81 p91)
		(downTo p81 p71)
		(leftTo p81 p82)
		(rightTo p81 p80)
		(oAt o83 p82)
		(upTo p82 p92)
		(downTo p82 p72)
		(leftTo p82 p83)
		(rightTo p82 p81)
		(posEmpty p83)
		(upTo p83 p93)
		(downTo p83 p73)
		(leftTo p83 p84)
		(rightTo p83 p82)
		(posEmpty p84)
		(upTo p84 p94)
		(downTo p84 p74)
		(leftTo p84 p85)
		(rightTo p84 p83)
		(posEmpty p85)
		(upTo p85 p95)
		(downTo p85 p75)
		(leftTo p85 p86)
		(rightTo p85 p84)
		(oAt o87 p86)
		(isLight o87)
		(isMoveable o87)
		(onGround o87)
		(clear o87)
		(upTo p86 p96)
		(downTo p86 p76)
		(leftTo p86 p87)
		(rightTo p86 p85)
		(posEmpty p87)
		(upTo p87 p97)
		(downTo p87 p77)
		(leftTo p87 p88)
		(rightTo p87 p86)
		(oAt o89 p88)
		(upTo p88 p98)
		(downTo p88 p78)
		(leftTo p88 p89)
		(rightTo p88 p87)
		(oAt o90 p89)
		(upTo p89 p99)
		(downTo p89 p79)
		(rightTo p89 p88)
		(oAt o91 p90)
		(downTo p90 p80)
		(leftTo p90 p91)
		(oAt o92 p91)
		(downTo p91 p81)
		(leftTo p91 p92)
		(rightTo p91 p90)
		(oAt o93 p92)
		(downTo p92 p82)
		(leftTo p92 p93)
		(rightTo p92 p91)
		(oAt o94 p93)
		(downTo p93 p83)
		(leftTo p93 p94)
		(rightTo p93 p92)
		(oAt o95 p94)
		(downTo p94 p84)
		(leftTo p94 p95)
		(rightTo p94 p93)
		(oAt o96 p95)
		(downTo p95 p85)
		(leftTo p95 p96)
		(rightTo p95 p94)
		(oAt o97 p96)
		(downTo p96 p86)
		(leftTo p96 p97)
		(rightTo p96 p95)
		(oAt o98 p97)
		(downTo p97 p87)
		(leftTo p97 p98)
		(rightTo p97 p96)
		(oAt o99 p98)
		(downTo p98 p88)
		(leftTo p98 p99)
		(rightTo p98 p97)
		(oAt o100 p99)
		(downTo p99 p89)
		(rightTo p99 p98)
    )
    (:goal
		(rAt r p64)
    )
    )