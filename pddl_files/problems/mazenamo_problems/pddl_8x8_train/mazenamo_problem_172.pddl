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
		p10 - pos
		p11 - pos
		p12 - pos
		p13 - pos
		p14 - pos
		p15 - pos
		o16 - obstacle
		p16 - pos
		o17 - obstacle
		p17 - pos
		p18 - pos
		p19 - pos
		o20 - obstacle
		p20 - pos
		o21 - obstacle
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
		o33 - obstacle
		p33 - pos
		o34 - obstacle
		p34 - pos
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
		p43 - pos
		p44 - pos
		p45 - pos
		p46 - pos
		p47 - pos
		o48 - obstacle
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
		o62 - obstacle
		p62 - pos
		o63 - obstacle
		p63 - pos
		o64 - obstacle
    )
    (:init
		(rAt r p34)
		(handempty)
		(dirIsDown r)
		(oAt o1 p0)
		(upTo p0 p8)
		(leftTo p0 p1)
		(oAt o2 p1)
		(upTo p1 p9)
		(leftTo p1 p2)
		(rightTo p1 p0)
		(oAt o3 p2)
		(upTo p2 p10)
		(leftTo p2 p3)
		(rightTo p2 p1)
		(oAt o4 p3)
		(upTo p3 p11)
		(leftTo p3 p4)
		(rightTo p3 p2)
		(oAt o5 p4)
		(upTo p4 p12)
		(leftTo p4 p5)
		(rightTo p4 p3)
		(oAt o6 p5)
		(upTo p5 p13)
		(leftTo p5 p6)
		(rightTo p5 p4)
		(oAt o7 p6)
		(upTo p6 p14)
		(leftTo p6 p7)
		(rightTo p6 p5)
		(oAt o8 p7)
		(upTo p7 p15)
		(rightTo p7 p6)
		(oAt o9 p8)
		(upTo p8 p16)
		(downTo p8 p0)
		(leftTo p8 p9)
		(posEmpty p9)
		(upTo p9 p17)
		(downTo p9 p1)
		(leftTo p9 p10)
		(rightTo p9 p8)
		(posEmpty p10)
		(upTo p10 p18)
		(downTo p10 p2)
		(leftTo p10 p11)
		(rightTo p10 p9)
		(posEmpty p11)
		(upTo p11 p19)
		(downTo p11 p3)
		(leftTo p11 p12)
		(rightTo p11 p10)
		(posEmpty p12)
		(upTo p12 p20)
		(downTo p12 p4)
		(leftTo p12 p13)
		(rightTo p12 p11)
		(posEmpty p13)
		(upTo p13 p21)
		(downTo p13 p5)
		(leftTo p13 p14)
		(rightTo p13 p12)
		(posEmpty p14)
		(upTo p14 p22)
		(downTo p14 p6)
		(leftTo p14 p15)
		(rightTo p14 p13)
		(oAt o16 p15)
		(upTo p15 p23)
		(downTo p15 p7)
		(rightTo p15 p14)
		(oAt o17 p16)
		(upTo p16 p24)
		(downTo p16 p8)
		(leftTo p16 p17)
		(posEmpty p17)
		(upTo p17 p25)
		(downTo p17 p9)
		(leftTo p17 p18)
		(rightTo p17 p16)
		(posEmpty p18)
		(upTo p18 p26)
		(downTo p18 p10)
		(leftTo p18 p19)
		(rightTo p18 p17)
		(oAt o20 p19)
		(isHeavy o20)
		(isMoveable o20)
		(onGround o20)
		(clear o20)
		(upTo p19 p27)
		(downTo p19 p11)
		(leftTo p19 p20)
		(rightTo p19 p18)
		(oAt o21 p20)
		(upTo p20 p28)
		(downTo p20 p12)
		(leftTo p20 p21)
		(rightTo p20 p19)
		(posEmpty p21)
		(upTo p21 p29)
		(downTo p21 p13)
		(leftTo p21 p22)
		(rightTo p21 p20)
		(oAt o23 p22)
		(upTo p22 p30)
		(downTo p22 p14)
		(leftTo p22 p23)
		(rightTo p22 p21)
		(oAt o24 p23)
		(upTo p23 p31)
		(downTo p23 p15)
		(rightTo p23 p22)
		(oAt o25 p24)
		(upTo p24 p32)
		(downTo p24 p16)
		(leftTo p24 p25)
		(oAt o26 p25)
		(isLight o26)
		(isMoveable o26)
		(onGround o26)
		(clear o26)
		(upTo p25 p33)
		(downTo p25 p17)
		(leftTo p25 p26)
		(rightTo p25 p24)
		(oAt o27 p26)
		(isLight o27)
		(isMoveable o27)
		(onGround o27)
		(clear o27)
		(upTo p26 p34)
		(downTo p26 p18)
		(leftTo p26 p27)
		(rightTo p26 p25)
		(oAt o28 p27)
		(upTo p27 p35)
		(downTo p27 p19)
		(leftTo p27 p28)
		(rightTo p27 p26)
		(posEmpty p28)
		(upTo p28 p36)
		(downTo p28 p20)
		(leftTo p28 p29)
		(rightTo p28 p27)
		(oAt o30 p29)
		(upTo p29 p37)
		(downTo p29 p21)
		(leftTo p29 p30)
		(rightTo p29 p28)
		(oAt o31 p30)
		(isHeavy o31)
		(isMoveable o31)
		(onGround o31)
		(clear o31)
		(upTo p30 p38)
		(downTo p30 p22)
		(leftTo p30 p31)
		(rightTo p30 p29)
		(oAt o32 p31)
		(upTo p31 p39)
		(downTo p31 p23)
		(rightTo p31 p30)
		(oAt o33 p32)
		(upTo p32 p40)
		(downTo p32 p24)
		(leftTo p32 p33)
		(oAt o34 p33)
		(upTo p33 p41)
		(downTo p33 p25)
		(leftTo p33 p34)
		(rightTo p33 p32)
		(posEmpty p34)
		(upTo p34 p42)
		(downTo p34 p26)
		(leftTo p34 p35)
		(rightTo p34 p33)
		(oAt o36 p35)
		(upTo p35 p43)
		(downTo p35 p27)
		(leftTo p35 p36)
		(rightTo p35 p34)
		(posEmpty p36)
		(upTo p36 p44)
		(downTo p36 p28)
		(leftTo p36 p37)
		(rightTo p36 p35)
		(posEmpty p37)
		(upTo p37 p45)
		(downTo p37 p29)
		(leftTo p37 p38)
		(rightTo p37 p36)
		(posEmpty p38)
		(upTo p38 p46)
		(downTo p38 p30)
		(leftTo p38 p39)
		(rightTo p38 p37)
		(oAt o40 p39)
		(upTo p39 p47)
		(downTo p39 p31)
		(rightTo p39 p38)
		(oAt o41 p40)
		(upTo p40 p48)
		(downTo p40 p32)
		(leftTo p40 p41)
		(posEmpty p41)
		(upTo p41 p49)
		(downTo p41 p33)
		(leftTo p41 p42)
		(rightTo p41 p40)
		(posEmpty p42)
		(upTo p42 p50)
		(downTo p42 p34)
		(leftTo p42 p43)
		(rightTo p42 p41)
		(posEmpty p43)
		(upTo p43 p51)
		(downTo p43 p35)
		(leftTo p43 p44)
		(rightTo p43 p42)
		(posEmpty p44)
		(upTo p44 p52)
		(downTo p44 p36)
		(leftTo p44 p45)
		(rightTo p44 p43)
		(posEmpty p45)
		(upTo p45 p53)
		(downTo p45 p37)
		(leftTo p45 p46)
		(rightTo p45 p44)
		(posEmpty p46)
		(upTo p46 p54)
		(downTo p46 p38)
		(leftTo p46 p47)
		(rightTo p46 p45)
		(oAt o48 p47)
		(upTo p47 p55)
		(downTo p47 p39)
		(rightTo p47 p46)
		(oAt o49 p48)
		(upTo p48 p56)
		(downTo p48 p40)
		(leftTo p48 p49)
		(oAt o50 p49)
		(upTo p49 p57)
		(downTo p49 p41)
		(leftTo p49 p50)
		(rightTo p49 p48)
		(oAt o51 p50)
		(upTo p50 p58)
		(downTo p50 p42)
		(leftTo p50 p51)
		(rightTo p50 p49)
		(posEmpty p51)
		(upTo p51 p59)
		(downTo p51 p43)
		(leftTo p51 p52)
		(rightTo p51 p50)
		(oAt o53 p52)
		(upTo p52 p60)
		(downTo p52 p44)
		(leftTo p52 p53)
		(rightTo p52 p51)
		(oAt o54 p53)
		(upTo p53 p61)
		(downTo p53 p45)
		(leftTo p53 p54)
		(rightTo p53 p52)
		(oAt o55 p54)
		(isHeavy o55)
		(isMoveable o55)
		(onGround o55)
		(clear o55)
		(upTo p54 p62)
		(downTo p54 p46)
		(leftTo p54 p55)
		(rightTo p54 p53)
		(oAt o56 p55)
		(upTo p55 p63)
		(downTo p55 p47)
		(rightTo p55 p54)
		(oAt o57 p56)
		(downTo p56 p48)
		(leftTo p56 p57)
		(oAt o58 p57)
		(downTo p57 p49)
		(leftTo p57 p58)
		(rightTo p57 p56)
		(oAt o59 p58)
		(downTo p58 p50)
		(leftTo p58 p59)
		(rightTo p58 p57)
		(oAt o60 p59)
		(downTo p59 p51)
		(leftTo p59 p60)
		(rightTo p59 p58)
		(oAt o61 p60)
		(downTo p60 p52)
		(leftTo p60 p61)
		(rightTo p60 p59)
		(oAt o62 p61)
		(downTo p61 p53)
		(leftTo p61 p62)
		(rightTo p61 p60)
		(oAt o63 p62)
		(downTo p62 p54)
		(leftTo p62 p63)
		(rightTo p62 p61)
		(oAt o64 p63)
		(downTo p63 p55)
		(rightTo p63 p62)
    )
    (:goal
		(rAt r p10)
    )
    )