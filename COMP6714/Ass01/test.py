answer ← ∅ ;
while p1 ≠ nil ∧ p2 ≠ nil do
	if docID(p1) = docID(p2) then
		l ← [ ];
		pp1 ← positions(p1); pp$ ← positions(p$);
		start = 0; end = pp$;
		range = [start, end];
		while pp1 ≠ nil do
			pp2 = skipTo(p2, docID(p2), pos(pp1));
			if pos(pp1) < pos(pp$)
				while pos(pp1) < pos(pp2) ∧ pos(pp1) ∈ range ∧ pos(pp2) ∈ range then
					add(l,pos(pp2));
					pp2 ← next(pp2);
				pp1 ← next(pp1);
				while l ≠ [ ] ∧ pos(pp1) > l[1] do
					delete(l[1]);
				for each ps ∈ l do
					answer ← answer ∪ [docID(p1),pos(pp1), ps];
			else
				l ← [ ];
				start = end;
				end = next(pp$);
				pp$ ← next(pp$);
	else
		p$ ← next(p$)
		if docID(p1) < docID(p2) then
			p1 ← next(p1);
		else
			p2 ← next(p2);
return answer;
