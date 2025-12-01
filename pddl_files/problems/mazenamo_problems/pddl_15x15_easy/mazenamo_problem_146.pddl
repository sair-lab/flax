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
		o14 - obstacle
		p14 - pos
		o15 - obstacle
		p15 - pos
		o16 - obstacle
		p16 - pos
		o17 - obstacle
		p17 - pos
		p18 - pos
		o19 - obstacle
		p19 - pos
		o20 - obstacle
		p20 - pos
		o21 - obstacle
		p21 - pos
		o22 - obstacle
		p22 - pos
		p23 - pos
		o24 - obstacle
		p24 - pos
		p25 - pos
		p26 - pos
		o27 - obstacle
		p27 - pos
		p28 - pos
		p29 - pos
		o30 - obstacle
		p30 - pos
		o31 - obstacle
		p31 - pos
		o32 - obstacle
		p32 - pos
		o33 - obstacle
		p33 - pos
		o34 - obstacle
		p34 - pos
		o35 - obstacle
		p35 - pos
		p36 - pos
		o37 - obstacle
		p37 - pos
		p38 - pos
		o39 - obstacle
		p39 - pos
		o40 - obstacle
		p40 - pos
		o41 - obstacle
		p41 - pos
		p42 - pos
		o43 - obstacle
		p43 - pos
		p44 - pos
		o45 - obstacle
		p45 - pos
		o46 - obstacle
		p46 - pos
		p47 - pos
		o48 - obstacle
		p48 - pos
		p49 - pos
		o50 - obstacle
		p50 - pos
		o51 - obstacle
		p51 - pos
		p52 - pos
		p53 - pos
		p54 - pos
		o55 - obstacle
		p55 - pos
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
		p64 - pos
		o65 - obstacle
		p65 - pos
		o66 - obstacle
		p66 - pos
		p67 - pos
		o68 - obstacle
		p68 - pos
		p69 - pos
		p70 - pos
		o71 - obstacle
		p71 - pos
		o72 - obstacle
		p72 - pos
		p73 - pos
		p74 - pos
		o75 - obstacle
		p75 - pos
		o76 - obstacle
		p76 - pos
		o77 - obstacle
		p77 - pos
		o78 - obstacle
		p78 - pos
		p79 - pos
		p80 - pos
		o81 - obstacle
		p81 - pos
		o82 - obstacle
		p82 - pos
		o83 - obstacle
		p83 - pos
		o84 - obstacle
		p84 - pos
		p85 - pos
		o86 - obstacle
		p86 - pos
		p87 - pos
		p88 - pos
		p89 - pos
		o90 - obstacle
		p90 - pos
		o91 - obstacle
		p91 - pos
		p92 - pos
		p93 - pos
		p94 - pos
		p95 - pos
		o96 - obstacle
		p96 - pos
		p97 - pos
		o98 - obstacle
		p98 - pos
		o99 - obstacle
		p99 - pos
		o100 - obstacle
		p100 - pos
		p101 - pos
		o102 - obstacle
		p102 - pos
		o103 - obstacle
		p103 - pos
		p104 - pos
		o105 - obstacle
		p105 - pos
		o106 - obstacle
		p106 - pos
		o107 - obstacle
		p107 - pos
		p108 - pos
		o109 - obstacle
		p109 - pos
		o110 - obstacle
		p110 - pos
		p111 - pos
		p112 - pos
		o113 - obstacle
		p113 - pos
		p114 - pos
		p115 - pos
		p116 - pos
		p117 - pos
		p118 - pos
		p119 - pos
		o120 - obstacle
		p120 - pos
		o121 - obstacle
		p121 - pos
		o122 - obstacle
		p122 - pos
		o123 - obstacle
		p123 - pos
		p124 - pos
		p125 - pos
		o126 - obstacle
		p126 - pos
		p127 - pos
		p128 - pos
		p129 - pos
		p130 - pos
		o131 - obstacle
		p131 - pos
		o132 - obstacle
		p132 - pos
		o133 - obstacle
		p133 - pos
		p134 - pos
		o135 - obstacle
		p135 - pos
		o136 - obstacle
		p136 - pos
		o137 - obstacle
		p137 - pos
		p138 - pos
		o139 - obstacle
		p139 - pos
		p140 - pos
		p141 - pos
		o142 - obstacle
		p142 - pos
		o143 - obstacle
		p143 - pos
		p144 - pos
		o145 - obstacle
		p145 - pos
		o146 - obstacle
		p146 - pos
		p147 - pos
		o148 - obstacle
		p148 - pos
		o149 - obstacle
		p149 - pos
		o150 - obstacle
		p150 - pos
		o151 - obstacle
		p151 - pos
		p152 - pos
		o153 - obstacle
		p153 - pos
		o154 - obstacle
		p154 - pos
		o155 - obstacle
		p155 - pos
		o156 - obstacle
		p156 - pos
		o157 - obstacle
		p157 - pos
		o158 - obstacle
		p158 - pos
		p159 - pos
		p160 - pos
		o161 - obstacle
		p161 - pos
		p162 - pos
		p163 - pos
		p164 - pos
		o165 - obstacle
		p165 - pos
		o166 - obstacle
		p166 - pos
		o167 - obstacle
		p167 - pos
		o168 - obstacle
		p168 - pos
		o169 - obstacle
		p169 - pos
		p170 - pos
		p171 - pos
		o172 - obstacle
		p172 - pos
		p173 - pos
		p174 - pos
		p175 - pos
		o176 - obstacle
		p176 - pos
		p177 - pos
		p178 - pos
		p179 - pos
		o180 - obstacle
		p180 - pos
		o181 - obstacle
		p181 - pos
		p182 - pos
		p183 - pos
		o184 - obstacle
		p184 - pos
		o185 - obstacle
		p185 - pos
		p186 - pos
		o187 - obstacle
		p187 - pos
		p188 - pos
		o189 - obstacle
		p189 - pos
		p190 - pos
		p191 - pos
		o192 - obstacle
		p192 - pos
		o193 - obstacle
		p193 - pos
		p194 - pos
		o195 - obstacle
		p195 - pos
		o196 - obstacle
		p196 - pos
		o197 - obstacle
		p197 - pos
		o198 - obstacle
		p198 - pos
		o199 - obstacle
		p199 - pos
		p200 - pos
		o201 - obstacle
		p201 - pos
		o202 - obstacle
		p202 - pos
		o203 - obstacle
		p203 - pos
		o204 - obstacle
		p204 - pos
		p205 - pos
		p206 - pos
		p207 - pos
		p208 - pos
		p209 - pos
		o210 - obstacle
		p210 - pos
		o211 - obstacle
		p211 - pos
		o212 - obstacle
		p212 - pos
		o213 - obstacle
		p213 - pos
		o214 - obstacle
		p214 - pos
		o215 - obstacle
		p215 - pos
		o216 - obstacle
		p216 - pos
		o217 - obstacle
		p217 - pos
		o218 - obstacle
		p218 - pos
		o219 - obstacle
		p219 - pos
		o220 - obstacle
		p220 - pos
		o221 - obstacle
		p221 - pos
		o222 - obstacle
		p222 - pos
		o223 - obstacle
		p223 - pos
		o224 - obstacle
		p224 - pos
		o225 - obstacle
    )
    (:init
		(rAt r p73)
		(handempty)
		(dirIsUp r)
		(oAt o1 p0)
		(upTo p0 p15)
		(leftTo p0 p1)
		(oAt o2 p1)
		(upTo p1 p16)
		(leftTo p1 p2)
		(rightTo p1 p0)
		(oAt o3 p2)
		(upTo p2 p17)
		(leftTo p2 p3)
		(rightTo p2 p1)
		(oAt o4 p3)
		(upTo p3 p18)
		(leftTo p3 p4)
		(rightTo p3 p2)
		(oAt o5 p4)
		(upTo p4 p19)
		(leftTo p4 p5)
		(rightTo p4 p3)
		(oAt o6 p5)
		(upTo p5 p20)
		(leftTo p5 p6)
		(rightTo p5 p4)
		(oAt o7 p6)
		(upTo p6 p21)
		(leftTo p6 p7)
		(rightTo p6 p5)
		(oAt o8 p7)
		(upTo p7 p22)
		(leftTo p7 p8)
		(rightTo p7 p6)
		(oAt o9 p8)
		(upTo p8 p23)
		(leftTo p8 p9)
		(rightTo p8 p7)
		(oAt o10 p9)
		(upTo p9 p24)
		(leftTo p9 p10)
		(rightTo p9 p8)
		(oAt o11 p10)
		(upTo p10 p25)
		(leftTo p10 p11)
		(rightTo p10 p9)
		(oAt o12 p11)
		(upTo p11 p26)
		(leftTo p11 p12)
		(rightTo p11 p10)
		(oAt o13 p12)
		(upTo p12 p27)
		(leftTo p12 p13)
		(rightTo p12 p11)
		(oAt o14 p13)
		(upTo p13 p28)
		(leftTo p13 p14)
		(rightTo p13 p12)
		(oAt o15 p14)
		(upTo p14 p29)
		(rightTo p14 p13)
		(oAt o16 p15)
		(upTo p15 p30)
		(downTo p15 p0)
		(leftTo p15 p16)
		(oAt o17 p16)
		(isLight o17)
		(isMoveable o17)
		(onGround o17)
		(clear o17)
		(upTo p16 p31)
		(downTo p16 p1)
		(leftTo p16 p17)
		(rightTo p16 p15)
		(posEmpty p17)
		(upTo p17 p32)
		(downTo p17 p2)
		(leftTo p17 p18)
		(rightTo p17 p16)
		(oAt o19 p18)
		(isLight o19)
		(isMoveable o19)
		(onGround o19)
		(clear o19)
		(upTo p18 p33)
		(downTo p18 p3)
		(leftTo p18 p19)
		(rightTo p18 p17)
		(oAt o20 p19)
		(upTo p19 p34)
		(downTo p19 p4)
		(leftTo p19 p20)
		(rightTo p19 p18)
		(oAt o21 p20)
		(isHeavy o21)
		(isMoveable o21)
		(onGround o21)
		(clear o21)
		(upTo p20 p35)
		(downTo p20 p5)
		(leftTo p20 p21)
		(rightTo p20 p19)
		(oAt o22 p21)
		(isHeavy o22)
		(isMoveable o22)
		(onGround o22)
		(clear o22)
		(upTo p21 p36)
		(downTo p21 p6)
		(leftTo p21 p22)
		(rightTo p21 p20)
		(posEmpty p22)
		(upTo p22 p37)
		(downTo p22 p7)
		(leftTo p22 p23)
		(rightTo p22 p21)
		(oAt o24 p23)
		(isLight o24)
		(isMoveable o24)
		(onGround o24)
		(clear o24)
		(upTo p23 p38)
		(downTo p23 p8)
		(leftTo p23 p24)
		(rightTo p23 p22)
		(posEmpty p24)
		(upTo p24 p39)
		(downTo p24 p9)
		(leftTo p24 p25)
		(rightTo p24 p23)
		(posEmpty p25)
		(upTo p25 p40)
		(downTo p25 p10)
		(leftTo p25 p26)
		(rightTo p25 p24)
		(oAt o27 p26)
		(isLight o27)
		(isMoveable o27)
		(onGround o27)
		(clear o27)
		(upTo p26 p41)
		(downTo p26 p11)
		(leftTo p26 p27)
		(rightTo p26 p25)
		(posEmpty p27)
		(upTo p27 p42)
		(downTo p27 p12)
		(leftTo p27 p28)
		(rightTo p27 p26)
		(posEmpty p28)
		(upTo p28 p43)
		(downTo p28 p13)
		(leftTo p28 p29)
		(rightTo p28 p27)
		(oAt o30 p29)
		(upTo p29 p44)
		(downTo p29 p14)
		(rightTo p29 p28)
		(oAt o31 p30)
		(upTo p30 p45)
		(downTo p30 p15)
		(leftTo p30 p31)
		(oAt o32 p31)
		(isLight o32)
		(isMoveable o32)
		(onGround o32)
		(clear o32)
		(upTo p31 p46)
		(downTo p31 p16)
		(leftTo p31 p32)
		(rightTo p31 p30)
		(oAt o33 p32)
		(upTo p32 p47)
		(downTo p32 p17)
		(leftTo p32 p33)
		(rightTo p32 p31)
		(oAt o34 p33)
		(isLight o34)
		(isMoveable o34)
		(onGround o34)
		(clear o34)
		(upTo p33 p48)
		(downTo p33 p18)
		(leftTo p33 p34)
		(rightTo p33 p32)
		(oAt o35 p34)
		(isLight o35)
		(isMoveable o35)
		(onGround o35)
		(clear o35)
		(upTo p34 p49)
		(downTo p34 p19)
		(leftTo p34 p35)
		(rightTo p34 p33)
		(posEmpty p35)
		(upTo p35 p50)
		(downTo p35 p20)
		(leftTo p35 p36)
		(rightTo p35 p34)
		(oAt o37 p36)
		(upTo p36 p51)
		(downTo p36 p21)
		(leftTo p36 p37)
		(rightTo p36 p35)
		(posEmpty p37)
		(upTo p37 p52)
		(downTo p37 p22)
		(leftTo p37 p38)
		(rightTo p37 p36)
		(oAt o39 p38)
		(isHeavy o39)
		(isMoveable o39)
		(onGround o39)
		(clear o39)
		(upTo p38 p53)
		(downTo p38 p23)
		(leftTo p38 p39)
		(rightTo p38 p37)
		(oAt o40 p39)
		(isLight o40)
		(isMoveable o40)
		(onGround o40)
		(clear o40)
		(upTo p39 p54)
		(downTo p39 p24)
		(leftTo p39 p40)
		(rightTo p39 p38)
		(oAt o41 p40)
		(isLight o41)
		(isMoveable o41)
		(onGround o41)
		(clear o41)
		(upTo p40 p55)
		(downTo p40 p25)
		(leftTo p40 p41)
		(rightTo p40 p39)
		(posEmpty p41)
		(upTo p41 p56)
		(downTo p41 p26)
		(leftTo p41 p42)
		(rightTo p41 p40)
		(oAt o43 p42)
		(isLight o43)
		(isMoveable o43)
		(onGround o43)
		(clear o43)
		(upTo p42 p57)
		(downTo p42 p27)
		(leftTo p42 p43)
		(rightTo p42 p41)
		(posEmpty p43)
		(upTo p43 p58)
		(downTo p43 p28)
		(leftTo p43 p44)
		(rightTo p43 p42)
		(oAt o45 p44)
		(upTo p44 p59)
		(downTo p44 p29)
		(rightTo p44 p43)
		(oAt o46 p45)
		(upTo p45 p60)
		(downTo p45 p30)
		(leftTo p45 p46)
		(posEmpty p46)
		(upTo p46 p61)
		(downTo p46 p31)
		(leftTo p46 p47)
		(rightTo p46 p45)
		(oAt o48 p47)
		(upTo p47 p62)
		(downTo p47 p32)
		(leftTo p47 p48)
		(rightTo p47 p46)
		(posEmpty p48)
		(upTo p48 p63)
		(downTo p48 p33)
		(leftTo p48 p49)
		(rightTo p48 p47)
		(oAt o50 p49)
		(isLight o50)
		(isMoveable o50)
		(onGround o50)
		(clear o50)
		(upTo p49 p64)
		(downTo p49 p34)
		(leftTo p49 p50)
		(rightTo p49 p48)
		(oAt o51 p50)
		(isLight o51)
		(isMoveable o51)
		(onGround o51)
		(clear o51)
		(upTo p50 p65)
		(downTo p50 p35)
		(leftTo p50 p51)
		(rightTo p50 p49)
		(posEmpty p51)
		(upTo p51 p66)
		(downTo p51 p36)
		(leftTo p51 p52)
		(rightTo p51 p50)
		(posEmpty p52)
		(upTo p52 p67)
		(downTo p52 p37)
		(leftTo p52 p53)
		(rightTo p52 p51)
		(posEmpty p53)
		(upTo p53 p68)
		(downTo p53 p38)
		(leftTo p53 p54)
		(rightTo p53 p52)
		(oAt o55 p54)
		(isLight o55)
		(isMoveable o55)
		(onGround o55)
		(clear o55)
		(upTo p54 p69)
		(downTo p54 p39)
		(leftTo p54 p55)
		(rightTo p54 p53)
		(posEmpty p55)
		(upTo p55 p70)
		(downTo p55 p40)
		(leftTo p55 p56)
		(rightTo p55 p54)
		(oAt o57 p56)
		(isHeavy o57)
		(isMoveable o57)
		(onGround o57)
		(clear o57)
		(upTo p56 p71)
		(downTo p56 p41)
		(leftTo p56 p57)
		(rightTo p56 p55)
		(oAt o58 p57)
		(isLight o58)
		(isMoveable o58)
		(onGround o58)
		(clear o58)
		(upTo p57 p72)
		(downTo p57 p42)
		(leftTo p57 p58)
		(rightTo p57 p56)
		(oAt o59 p58)
		(upTo p58 p73)
		(downTo p58 p43)
		(leftTo p58 p59)
		(rightTo p58 p57)
		(oAt o60 p59)
		(upTo p59 p74)
		(downTo p59 p44)
		(rightTo p59 p58)
		(oAt o61 p60)
		(upTo p60 p75)
		(downTo p60 p45)
		(leftTo p60 p61)
		(posEmpty p61)
		(upTo p61 p76)
		(downTo p61 p46)
		(leftTo p61 p62)
		(rightTo p61 p60)
		(oAt o63 p62)
		(isLight o63)
		(isMoveable o63)
		(onGround o63)
		(clear o63)
		(upTo p62 p77)
		(downTo p62 p47)
		(leftTo p62 p63)
		(rightTo p62 p61)
		(posEmpty p63)
		(upTo p63 p78)
		(downTo p63 p48)
		(leftTo p63 p64)
		(rightTo p63 p62)
		(oAt o65 p64)
		(upTo p64 p79)
		(downTo p64 p49)
		(leftTo p64 p65)
		(rightTo p64 p63)
		(oAt o66 p65)
		(isHeavy o66)
		(isMoveable o66)
		(onGround o66)
		(clear o66)
		(upTo p65 p80)
		(downTo p65 p50)
		(leftTo p65 p66)
		(rightTo p65 p64)
		(posEmpty p66)
		(upTo p66 p81)
		(downTo p66 p51)
		(leftTo p66 p67)
		(rightTo p66 p65)
		(oAt o68 p67)
		(upTo p67 p82)
		(downTo p67 p52)
		(leftTo p67 p68)
		(rightTo p67 p66)
		(posEmpty p68)
		(upTo p68 p83)
		(downTo p68 p53)
		(leftTo p68 p69)
		(rightTo p68 p67)
		(posEmpty p69)
		(upTo p69 p84)
		(downTo p69 p54)
		(leftTo p69 p70)
		(rightTo p69 p68)
		(oAt o71 p70)
		(isLight o71)
		(isMoveable o71)
		(onGround o71)
		(clear o71)
		(upTo p70 p85)
		(downTo p70 p55)
		(leftTo p70 p71)
		(rightTo p70 p69)
		(oAt o72 p71)
		(upTo p71 p86)
		(downTo p71 p56)
		(leftTo p71 p72)
		(rightTo p71 p70)
		(posEmpty p72)
		(upTo p72 p87)
		(downTo p72 p57)
		(leftTo p72 p73)
		(rightTo p72 p71)
		(posEmpty p73)
		(upTo p73 p88)
		(downTo p73 p58)
		(leftTo p73 p74)
		(rightTo p73 p72)
		(oAt o75 p74)
		(upTo p74 p89)
		(downTo p74 p59)
		(rightTo p74 p73)
		(oAt o76 p75)
		(upTo p75 p90)
		(downTo p75 p60)
		(leftTo p75 p76)
		(oAt o77 p76)
		(isLight o77)
		(isMoveable o77)
		(onGround o77)
		(clear o77)
		(upTo p76 p91)
		(downTo p76 p61)
		(leftTo p76 p77)
		(rightTo p76 p75)
		(oAt o78 p77)
		(isLight o78)
		(isMoveable o78)
		(onGround o78)
		(clear o78)
		(upTo p77 p92)
		(downTo p77 p62)
		(leftTo p77 p78)
		(rightTo p77 p76)
		(posEmpty p78)
		(upTo p78 p93)
		(downTo p78 p63)
		(leftTo p78 p79)
		(rightTo p78 p77)
		(posEmpty p79)
		(upTo p79 p94)
		(downTo p79 p64)
		(leftTo p79 p80)
		(rightTo p79 p78)
		(oAt o81 p80)
		(isLight o81)
		(isMoveable o81)
		(onGround o81)
		(clear o81)
		(upTo p80 p95)
		(downTo p80 p65)
		(leftTo p80 p81)
		(rightTo p80 p79)
		(oAt o82 p81)
		(isLight o82)
		(isMoveable o82)
		(onGround o82)
		(clear o82)
		(upTo p81 p96)
		(downTo p81 p66)
		(leftTo p81 p82)
		(rightTo p81 p80)
		(oAt o83 p82)
		(upTo p82 p97)
		(downTo p82 p67)
		(leftTo p82 p83)
		(rightTo p82 p81)
		(oAt o84 p83)
		(upTo p83 p98)
		(downTo p83 p68)
		(leftTo p83 p84)
		(rightTo p83 p82)
		(posEmpty p84)
		(upTo p84 p99)
		(downTo p84 p69)
		(leftTo p84 p85)
		(rightTo p84 p83)
		(oAt o86 p85)
		(upTo p85 p100)
		(downTo p85 p70)
		(leftTo p85 p86)
		(rightTo p85 p84)
		(posEmpty p86)
		(upTo p86 p101)
		(downTo p86 p71)
		(leftTo p86 p87)
		(rightTo p86 p85)
		(posEmpty p87)
		(upTo p87 p102)
		(downTo p87 p72)
		(leftTo p87 p88)
		(rightTo p87 p86)
		(posEmpty p88)
		(upTo p88 p103)
		(downTo p88 p73)
		(leftTo p88 p89)
		(rightTo p88 p87)
		(oAt o90 p89)
		(upTo p89 p104)
		(downTo p89 p74)
		(rightTo p89 p88)
		(oAt o91 p90)
		(upTo p90 p105)
		(downTo p90 p75)
		(leftTo p90 p91)
		(posEmpty p91)
		(upTo p91 p106)
		(downTo p91 p76)
		(leftTo p91 p92)
		(rightTo p91 p90)
		(posEmpty p92)
		(upTo p92 p107)
		(downTo p92 p77)
		(leftTo p92 p93)
		(rightTo p92 p91)
		(posEmpty p93)
		(upTo p93 p108)
		(downTo p93 p78)
		(leftTo p93 p94)
		(rightTo p93 p92)
		(posEmpty p94)
		(upTo p94 p109)
		(downTo p94 p79)
		(leftTo p94 p95)
		(rightTo p94 p93)
		(oAt o96 p95)
		(isLight o96)
		(isMoveable o96)
		(onGround o96)
		(clear o96)
		(upTo p95 p110)
		(downTo p95 p80)
		(leftTo p95 p96)
		(rightTo p95 p94)
		(posEmpty p96)
		(upTo p96 p111)
		(downTo p96 p81)
		(leftTo p96 p97)
		(rightTo p96 p95)
		(oAt o98 p97)
		(upTo p97 p112)
		(downTo p97 p82)
		(leftTo p97 p98)
		(rightTo p97 p96)
		(oAt o99 p98)
		(isLight o99)
		(isMoveable o99)
		(onGround o99)
		(clear o99)
		(upTo p98 p113)
		(downTo p98 p83)
		(leftTo p98 p99)
		(rightTo p98 p97)
		(oAt o100 p99)
		(upTo p99 p114)
		(downTo p99 p84)
		(leftTo p99 p100)
		(rightTo p99 p98)
		(posEmpty p100)
		(upTo p100 p115)
		(downTo p100 p85)
		(leftTo p100 p101)
		(rightTo p100 p99)
		(oAt o102 p101)
		(isLight o102)
		(isMoveable o102)
		(onGround o102)
		(clear o102)
		(upTo p101 p116)
		(downTo p101 p86)
		(leftTo p101 p102)
		(rightTo p101 p100)
		(oAt o103 p102)
		(upTo p102 p117)
		(downTo p102 p87)
		(leftTo p102 p103)
		(rightTo p102 p101)
		(posEmpty p103)
		(upTo p103 p118)
		(downTo p103 p88)
		(leftTo p103 p104)
		(rightTo p103 p102)
		(oAt o105 p104)
		(upTo p104 p119)
		(downTo p104 p89)
		(rightTo p104 p103)
		(oAt o106 p105)
		(upTo p105 p120)
		(downTo p105 p90)
		(leftTo p105 p106)
		(oAt o107 p106)
		(upTo p106 p121)
		(downTo p106 p91)
		(leftTo p106 p107)
		(rightTo p106 p105)
		(posEmpty p107)
		(upTo p107 p122)
		(downTo p107 p92)
		(leftTo p107 p108)
		(rightTo p107 p106)
		(oAt o109 p108)
		(isLight o109)
		(isMoveable o109)
		(onGround o109)
		(clear o109)
		(upTo p108 p123)
		(downTo p108 p93)
		(leftTo p108 p109)
		(rightTo p108 p107)
		(oAt o110 p109)
		(upTo p109 p124)
		(downTo p109 p94)
		(leftTo p109 p110)
		(rightTo p109 p108)
		(posEmpty p110)
		(upTo p110 p125)
		(downTo p110 p95)
		(leftTo p110 p111)
		(rightTo p110 p109)
		(posEmpty p111)
		(upTo p111 p126)
		(downTo p111 p96)
		(leftTo p111 p112)
		(rightTo p111 p110)
		(oAt o113 p112)
		(isHeavy o113)
		(isMoveable o113)
		(onGround o113)
		(clear o113)
		(upTo p112 p127)
		(downTo p112 p97)
		(leftTo p112 p113)
		(rightTo p112 p111)
		(posEmpty p113)
		(upTo p113 p128)
		(downTo p113 p98)
		(leftTo p113 p114)
		(rightTo p113 p112)
		(posEmpty p114)
		(upTo p114 p129)
		(downTo p114 p99)
		(leftTo p114 p115)
		(rightTo p114 p113)
		(posEmpty p115)
		(upTo p115 p130)
		(downTo p115 p100)
		(leftTo p115 p116)
		(rightTo p115 p114)
		(posEmpty p116)
		(upTo p116 p131)
		(downTo p116 p101)
		(leftTo p116 p117)
		(rightTo p116 p115)
		(posEmpty p117)
		(upTo p117 p132)
		(downTo p117 p102)
		(leftTo p117 p118)
		(rightTo p117 p116)
		(posEmpty p118)
		(upTo p118 p133)
		(downTo p118 p103)
		(leftTo p118 p119)
		(rightTo p118 p117)
		(oAt o120 p119)
		(upTo p119 p134)
		(downTo p119 p104)
		(rightTo p119 p118)
		(oAt o121 p120)
		(upTo p120 p135)
		(downTo p120 p105)
		(leftTo p120 p121)
		(oAt o122 p121)
		(upTo p121 p136)
		(downTo p121 p106)
		(leftTo p121 p122)
		(rightTo p121 p120)
		(oAt o123 p122)
		(isLight o123)
		(isMoveable o123)
		(onGround o123)
		(clear o123)
		(upTo p122 p137)
		(downTo p122 p107)
		(leftTo p122 p123)
		(rightTo p122 p121)
		(posEmpty p123)
		(upTo p123 p138)
		(downTo p123 p108)
		(leftTo p123 p124)
		(rightTo p123 p122)
		(posEmpty p124)
		(upTo p124 p139)
		(downTo p124 p109)
		(leftTo p124 p125)
		(rightTo p124 p123)
		(oAt o126 p125)
		(isLight o126)
		(isMoveable o126)
		(onGround o126)
		(clear o126)
		(upTo p125 p140)
		(downTo p125 p110)
		(leftTo p125 p126)
		(rightTo p125 p124)
		(posEmpty p126)
		(upTo p126 p141)
		(downTo p126 p111)
		(leftTo p126 p127)
		(rightTo p126 p125)
		(posEmpty p127)
		(upTo p127 p142)
		(downTo p127 p112)
		(leftTo p127 p128)
		(rightTo p127 p126)
		(posEmpty p128)
		(upTo p128 p143)
		(downTo p128 p113)
		(leftTo p128 p129)
		(rightTo p128 p127)
		(posEmpty p129)
		(upTo p129 p144)
		(downTo p129 p114)
		(leftTo p129 p130)
		(rightTo p129 p128)
		(oAt o131 p130)
		(isLight o131)
		(isMoveable o131)
		(onGround o131)
		(clear o131)
		(upTo p130 p145)
		(downTo p130 p115)
		(leftTo p130 p131)
		(rightTo p130 p129)
		(oAt o132 p131)
		(upTo p131 p146)
		(downTo p131 p116)
		(leftTo p131 p132)
		(rightTo p131 p130)
		(oAt o133 p132)
		(upTo p132 p147)
		(downTo p132 p117)
		(leftTo p132 p133)
		(rightTo p132 p131)
		(posEmpty p133)
		(upTo p133 p148)
		(downTo p133 p118)
		(leftTo p133 p134)
		(rightTo p133 p132)
		(oAt o135 p134)
		(upTo p134 p149)
		(downTo p134 p119)
		(rightTo p134 p133)
		(oAt o136 p135)
		(upTo p135 p150)
		(downTo p135 p120)
		(leftTo p135 p136)
		(oAt o137 p136)
		(upTo p136 p151)
		(downTo p136 p121)
		(leftTo p136 p137)
		(rightTo p136 p135)
		(posEmpty p137)
		(upTo p137 p152)
		(downTo p137 p122)
		(leftTo p137 p138)
		(rightTo p137 p136)
		(oAt o139 p138)
		(upTo p138 p153)
		(downTo p138 p123)
		(leftTo p138 p139)
		(rightTo p138 p137)
		(posEmpty p139)
		(upTo p139 p154)
		(downTo p139 p124)
		(leftTo p139 p140)
		(rightTo p139 p138)
		(posEmpty p140)
		(upTo p140 p155)
		(downTo p140 p125)
		(leftTo p140 p141)
		(rightTo p140 p139)
		(oAt o142 p141)
		(upTo p141 p156)
		(downTo p141 p126)
		(leftTo p141 p142)
		(rightTo p141 p140)
		(oAt o143 p142)
		(isLight o143)
		(isMoveable o143)
		(onGround o143)
		(clear o143)
		(upTo p142 p157)
		(downTo p142 p127)
		(leftTo p142 p143)
		(rightTo p142 p141)
		(posEmpty p143)
		(upTo p143 p158)
		(downTo p143 p128)
		(leftTo p143 p144)
		(rightTo p143 p142)
		(oAt o145 p144)
		(upTo p144 p159)
		(downTo p144 p129)
		(leftTo p144 p145)
		(rightTo p144 p143)
		(oAt o146 p145)
		(isLight o146)
		(isMoveable o146)
		(onGround o146)
		(clear o146)
		(upTo p145 p160)
		(downTo p145 p130)
		(leftTo p145 p146)
		(rightTo p145 p144)
		(posEmpty p146)
		(upTo p146 p161)
		(downTo p146 p131)
		(leftTo p146 p147)
		(rightTo p146 p145)
		(oAt o148 p147)
		(isLight o148)
		(isMoveable o148)
		(onGround o148)
		(clear o148)
		(upTo p147 p162)
		(downTo p147 p132)
		(leftTo p147 p148)
		(rightTo p147 p146)
		(oAt o149 p148)
		(upTo p148 p163)
		(downTo p148 p133)
		(leftTo p148 p149)
		(rightTo p148 p147)
		(oAt o150 p149)
		(upTo p149 p164)
		(downTo p149 p134)
		(rightTo p149 p148)
		(oAt o151 p150)
		(upTo p150 p165)
		(downTo p150 p135)
		(leftTo p150 p151)
		(posEmpty p151)
		(upTo p151 p166)
		(downTo p151 p136)
		(leftTo p151 p152)
		(rightTo p151 p150)
		(oAt o153 p152)
		(upTo p152 p167)
		(downTo p152 p137)
		(leftTo p152 p153)
		(rightTo p152 p151)
		(oAt o154 p153)
		(isLight o154)
		(isMoveable o154)
		(onGround o154)
		(clear o154)
		(upTo p153 p168)
		(downTo p153 p138)
		(leftTo p153 p154)
		(rightTo p153 p152)
		(oAt o155 p154)
		(upTo p154 p169)
		(downTo p154 p139)
		(leftTo p154 p155)
		(rightTo p154 p153)
		(oAt o156 p155)
		(isLight o156)
		(isMoveable o156)
		(onGround o156)
		(clear o156)
		(upTo p155 p170)
		(downTo p155 p140)
		(leftTo p155 p156)
		(rightTo p155 p154)
		(oAt o157 p156)
		(isLight o157)
		(isMoveable o157)
		(onGround o157)
		(clear o157)
		(upTo p156 p171)
		(downTo p156 p141)
		(leftTo p156 p157)
		(rightTo p156 p155)
		(oAt o158 p157)
		(upTo p157 p172)
		(downTo p157 p142)
		(leftTo p157 p158)
		(rightTo p157 p156)
		(posEmpty p158)
		(upTo p158 p173)
		(downTo p158 p143)
		(leftTo p158 p159)
		(rightTo p158 p157)
		(posEmpty p159)
		(upTo p159 p174)
		(downTo p159 p144)
		(leftTo p159 p160)
		(rightTo p159 p158)
		(oAt o161 p160)
		(isLight o161)
		(isMoveable o161)
		(onGround o161)
		(clear o161)
		(upTo p160 p175)
		(downTo p160 p145)
		(leftTo p160 p161)
		(rightTo p160 p159)
		(posEmpty p161)
		(upTo p161 p176)
		(downTo p161 p146)
		(leftTo p161 p162)
		(rightTo p161 p160)
		(posEmpty p162)
		(upTo p162 p177)
		(downTo p162 p147)
		(leftTo p162 p163)
		(rightTo p162 p161)
		(posEmpty p163)
		(upTo p163 p178)
		(downTo p163 p148)
		(leftTo p163 p164)
		(rightTo p163 p162)
		(oAt o165 p164)
		(upTo p164 p179)
		(downTo p164 p149)
		(rightTo p164 p163)
		(oAt o166 p165)
		(upTo p165 p180)
		(downTo p165 p150)
		(leftTo p165 p166)
		(oAt o167 p166)
		(isHeavy o167)
		(isMoveable o167)
		(onGround o167)
		(clear o167)
		(upTo p166 p181)
		(downTo p166 p151)
		(leftTo p166 p167)
		(rightTo p166 p165)
		(oAt o168 p167)
		(isLight o168)
		(isMoveable o168)
		(onGround o168)
		(clear o168)
		(upTo p167 p182)
		(downTo p167 p152)
		(leftTo p167 p168)
		(rightTo p167 p166)
		(oAt o169 p168)
		(isLight o169)
		(isMoveable o169)
		(onGround o169)
		(clear o169)
		(upTo p168 p183)
		(downTo p168 p153)
		(leftTo p168 p169)
		(rightTo p168 p167)
		(posEmpty p169)
		(upTo p169 p184)
		(downTo p169 p154)
		(leftTo p169 p170)
		(rightTo p169 p168)
		(posEmpty p170)
		(upTo p170 p185)
		(downTo p170 p155)
		(leftTo p170 p171)
		(rightTo p170 p169)
		(oAt o172 p171)
		(isLight o172)
		(isMoveable o172)
		(onGround o172)
		(clear o172)
		(upTo p171 p186)
		(downTo p171 p156)
		(leftTo p171 p172)
		(rightTo p171 p170)
		(posEmpty p172)
		(upTo p172 p187)
		(downTo p172 p157)
		(leftTo p172 p173)
		(rightTo p172 p171)
		(posEmpty p173)
		(upTo p173 p188)
		(downTo p173 p158)
		(leftTo p173 p174)
		(rightTo p173 p172)
		(posEmpty p174)
		(upTo p174 p189)
		(downTo p174 p159)
		(leftTo p174 p175)
		(rightTo p174 p173)
		(oAt o176 p175)
		(upTo p175 p190)
		(downTo p175 p160)
		(leftTo p175 p176)
		(rightTo p175 p174)
		(posEmpty p176)
		(upTo p176 p191)
		(downTo p176 p161)
		(leftTo p176 p177)
		(rightTo p176 p175)
		(posEmpty p177)
		(upTo p177 p192)
		(downTo p177 p162)
		(leftTo p177 p178)
		(rightTo p177 p176)
		(posEmpty p178)
		(upTo p178 p193)
		(downTo p178 p163)
		(leftTo p178 p179)
		(rightTo p178 p177)
		(oAt o180 p179)
		(upTo p179 p194)
		(downTo p179 p164)
		(rightTo p179 p178)
		(oAt o181 p180)
		(upTo p180 p195)
		(downTo p180 p165)
		(leftTo p180 p181)
		(posEmpty p181)
		(upTo p181 p196)
		(downTo p181 p166)
		(leftTo p181 p182)
		(rightTo p181 p180)
		(posEmpty p182)
		(upTo p182 p197)
		(downTo p182 p167)
		(leftTo p182 p183)
		(rightTo p182 p181)
		(oAt o184 p183)
		(upTo p183 p198)
		(downTo p183 p168)
		(leftTo p183 p184)
		(rightTo p183 p182)
		(oAt o185 p184)
		(upTo p184 p199)
		(downTo p184 p169)
		(leftTo p184 p185)
		(rightTo p184 p183)
		(posEmpty p185)
		(upTo p185 p200)
		(downTo p185 p170)
		(leftTo p185 p186)
		(rightTo p185 p184)
		(oAt o187 p186)
		(isHeavy o187)
		(isMoveable o187)
		(onGround o187)
		(clear o187)
		(upTo p186 p201)
		(downTo p186 p171)
		(leftTo p186 p187)
		(rightTo p186 p185)
		(posEmpty p187)
		(upTo p187 p202)
		(downTo p187 p172)
		(leftTo p187 p188)
		(rightTo p187 p186)
		(oAt o189 p188)
		(upTo p188 p203)
		(downTo p188 p173)
		(leftTo p188 p189)
		(rightTo p188 p187)
		(posEmpty p189)
		(upTo p189 p204)
		(downTo p189 p174)
		(leftTo p189 p190)
		(rightTo p189 p188)
		(posEmpty p190)
		(upTo p190 p205)
		(downTo p190 p175)
		(leftTo p190 p191)
		(rightTo p190 p189)
		(oAt o192 p191)
		(isHeavy o192)
		(isMoveable o192)
		(onGround o192)
		(clear o192)
		(upTo p191 p206)
		(downTo p191 p176)
		(leftTo p191 p192)
		(rightTo p191 p190)
		(oAt o193 p192)
		(upTo p192 p207)
		(downTo p192 p177)
		(leftTo p192 p193)
		(rightTo p192 p191)
		(posEmpty p193)
		(upTo p193 p208)
		(downTo p193 p178)
		(leftTo p193 p194)
		(rightTo p193 p192)
		(oAt o195 p194)
		(upTo p194 p209)
		(downTo p194 p179)
		(rightTo p194 p193)
		(oAt o196 p195)
		(upTo p195 p210)
		(downTo p195 p180)
		(leftTo p195 p196)
		(oAt o197 p196)
		(isLight o197)
		(isMoveable o197)
		(onGround o197)
		(clear o197)
		(upTo p196 p211)
		(downTo p196 p181)
		(leftTo p196 p197)
		(rightTo p196 p195)
		(oAt o198 p197)
		(upTo p197 p212)
		(downTo p197 p182)
		(leftTo p197 p198)
		(rightTo p197 p196)
		(oAt o199 p198)
		(isLight o199)
		(isMoveable o199)
		(onGround o199)
		(clear o199)
		(upTo p198 p213)
		(downTo p198 p183)
		(leftTo p198 p199)
		(rightTo p198 p197)
		(posEmpty p199)
		(upTo p199 p214)
		(downTo p199 p184)
		(leftTo p199 p200)
		(rightTo p199 p198)
		(oAt o201 p200)
		(upTo p200 p215)
		(downTo p200 p185)
		(leftTo p200 p201)
		(rightTo p200 p199)
		(oAt o202 p201)
		(isLight o202)
		(isMoveable o202)
		(onGround o202)
		(clear o202)
		(upTo p201 p216)
		(downTo p201 p186)
		(leftTo p201 p202)
		(rightTo p201 p200)
		(oAt o203 p202)
		(upTo p202 p217)
		(downTo p202 p187)
		(leftTo p202 p203)
		(rightTo p202 p201)
		(oAt o204 p203)
		(upTo p203 p218)
		(downTo p203 p188)
		(leftTo p203 p204)
		(rightTo p203 p202)
		(posEmpty p204)
		(upTo p204 p219)
		(downTo p204 p189)
		(leftTo p204 p205)
		(rightTo p204 p203)
		(posEmpty p205)
		(upTo p205 p220)
		(downTo p205 p190)
		(leftTo p205 p206)
		(rightTo p205 p204)
		(posEmpty p206)
		(upTo p206 p221)
		(downTo p206 p191)
		(leftTo p206 p207)
		(rightTo p206 p205)
		(posEmpty p207)
		(upTo p207 p222)
		(downTo p207 p192)
		(leftTo p207 p208)
		(rightTo p207 p206)
		(posEmpty p208)
		(upTo p208 p223)
		(downTo p208 p193)
		(leftTo p208 p209)
		(rightTo p208 p207)
		(oAt o210 p209)
		(upTo p209 p224)
		(downTo p209 p194)
		(rightTo p209 p208)
		(oAt o211 p210)
		(downTo p210 p195)
		(leftTo p210 p211)
		(oAt o212 p211)
		(downTo p211 p196)
		(leftTo p211 p212)
		(rightTo p211 p210)
		(oAt o213 p212)
		(downTo p212 p197)
		(leftTo p212 p213)
		(rightTo p212 p211)
		(oAt o214 p213)
		(downTo p213 p198)
		(leftTo p213 p214)
		(rightTo p213 p212)
		(oAt o215 p214)
		(downTo p214 p199)
		(leftTo p214 p215)
		(rightTo p214 p213)
		(oAt o216 p215)
		(downTo p215 p200)
		(leftTo p215 p216)
		(rightTo p215 p214)
		(oAt o217 p216)
		(downTo p216 p201)
		(leftTo p216 p217)
		(rightTo p216 p215)
		(oAt o218 p217)
		(downTo p217 p202)
		(leftTo p217 p218)
		(rightTo p217 p216)
		(oAt o219 p218)
		(downTo p218 p203)
		(leftTo p218 p219)
		(rightTo p218 p217)
		(oAt o220 p219)
		(downTo p219 p204)
		(leftTo p219 p220)
		(rightTo p219 p218)
		(oAt o221 p220)
		(downTo p220 p205)
		(leftTo p220 p221)
		(rightTo p220 p219)
		(oAt o222 p221)
		(downTo p221 p206)
		(leftTo p221 p222)
		(rightTo p221 p220)
		(oAt o223 p222)
		(downTo p222 p207)
		(leftTo p222 p223)
		(rightTo p222 p221)
		(oAt o224 p223)
		(downTo p223 p208)
		(leftTo p223 p224)
		(rightTo p223 p222)
		(oAt o225 p224)
		(downTo p224 p209)
		(rightTo p224 p223)
    )
    (:goal
		(rAt r p182)
    )
    )