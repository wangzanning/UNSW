-- comp9311 19T3 Project 1
--
-- MyMyUNSW Solutions


-- Q1:
create or replace view Q1(unswid, longname)
as 
select distinct ro.unswid, ro.longname
from rooms ro join room_facilities rf on rf.room = ro.id
	join facilities fa on fa.id = rf.facility
where fa.description = 'Air-conditioned';

--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q2:
create or replace view Q2_course_1(course)
as select course from course_enrolments ce
	join people p1 on p.id = ce.student
where p1.name = 'Hemma Margareta';

create or replace view Q2(unswid,name)
as select distinct p2.unswid, p2.name from people p2
	join course_staff cs on cs.staff = p2.id
	join Q2_course_1 on cs.course = Q2_course_1.course

--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q3:
create or replace view Q3_intl_1(sid,stype)
as select st.id as sid, st.stype from students st
where st.stype = 'intl';

create or replace view Q3_9311(sid,tid,name,code)
as select Q3_intl_1.sid, Q3_intl_1.stype, se.id as tid, su.code, ce.mark from Q3_intl_1
	join course_enrolments ce on ce.student = Q3_intl_1.sid
	join courses co on co.id = ce.course
	join subjects su on su.id = co.subject
	join semesters se on se.id = co.semester
where su.code = 'COMP9311' and ce.mark >=85;

create or replace view Q3_9024(sid,tid,name,code)
as select Q3_intl_1.sid, Q3_intl_1.stype, se.id as tid, su.code, ce.mark from Q3_intl_1
	join course_enrolments ce on ce.student = Q3_intl_1.sid
	join courses co on co.id = ce.course
	join subjects su on su.id = co.subject
	join semesters se on se.id = co.semester
where su.code = 'COMP9024' and ce.mark >=85;

create or replace view Q3_same(sid,tid)
as select Q3_9311.sid, Q3_9311.tid
from Q3_9311
intersect
select Q3_9024.sid, Q3_9024.tid
from Q3_9024;

create or replace view Q3(unswid, name)
as select pe.unswid, pe.name from people pe
	join Q3_same on Q3_same.sid = pe.id;
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q4:
create or replace view Q4_HD(student,HDcount)
as select distinct ce.student, count(ce.grade)as HDcount from course_enrolments ce
where ce.grade = 'HD'
group by ce.student;

create or replace view Q4_sumHD(sumHD)
as select count(ce.grade) as sumHD
from course_enrolments ce
where ce.grade = 'HD';

create or replace view Q4_sumStu(sumStu)
as select count(distinct ce.student) as sumStu from course_enrolments ce
where ce.grade is not null;

create or replace view Q4_aver(aver)
as select Q4_sumHD.sumHD/Q4_sumStu.sumStu as aver from Q4_sumHD,Q4_sumStu;


create or replace view Q4(num_student)
as select count(*) as num_student from Q4_HD,Q4_aver
where Q4_HD.HDcount > Q4_aver.aver;
--... SQL statements, possibly using other views/functions defined by you ...
;

--Q5:
create or replace view Q5_valid(course,numb)
as select ce.course as course,count(ce.course) as numb from course_enrolments ce
where ce.mark is not null group by ce.course;

create or replace view Q5_20(course,numb)
as select Q5_valid.course, Q5_valid.numb from Q5_valid
where Q5_valid.numb >= 20
order by numb desc; 

create or replace view Q5_classes(code,subname,semid,semname,mark_max)
as select distinct su.code, su.name as subname, sem.id as semid, sem.name as semname,max(ce.mark) as mark_max from courses co
	join subjects su on co.subject = su.id
	join course_enrolments ce on ce.course = co.id
	join semesters sem on co.semester = sem.id
	join Q5_20 on Q5_20.course = co.id
	group by su.name,su.code,sem.name,sem.id
order by mark_max;

create or replace view Q5_minmark(semname,semid,mark_min)
as select Q5_classes.semname,Q5_classes.semid,min(mark_max) as mark_min from Q5_classes
group by Q5_classes.semname,Q5_classes.semid
order by mark_min;  


create or replace view Q5(code, name, semester)
as select Q5_classes.code , Q5_classes.subname as name ,Q5_classes.semname as semester from Q5_classes
	join Q5_minmark on Q5_minmark.mark_min = Q5_classes.mark_max
	and Q5_minmark.semname = Q5_classes.semname
order by code desc; 

--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q6:
create or replace view Q6_2010_s1_1(p_unswid,year,term)
as select distinct p1.unswid as p_unswid ,se.year,se.term from people p1
	join students st on st.id = p1.id 
	join program_enrolments pe on pe.student = st.id
	join semesters se on se.id = pe.semester
where se.year = 2010 and se.term = 'S1';

create or replace view Q6_Intl_man_2(unswid, name, stype)
as select distinct Q6_2010_s1_1.p_unswid,st.stype,str.name from Q6_2010_s1_1
	join people p1 on p1.unswid = Q6_2010_s1_1.p_unswid
	join students st on st.id = p1.id
	join program_enrolments pe on pe.student = st.id
	join stream_enrolments se on se.partof = pe.id
	join streams str on str.id = se.stream
	join semesters sem on sem.id = pe.semester
where st.stype = 'local' and str.name = 'Management' and sem.year = 2010 and sem.term = 'S1';

create or replace view Q6_eng_3(unswid,orgun_name)
as select distinct p1.unswid,org.name from people p1
	join course_enrolments ce on ce.student = p1.id 
	join courses co on co.id = ce.course
	join subjects su on su.id = co.subject
	join orgunits org on org.id = su.offeredby
where org.name = 'Faculty of Engineering';

create or replace view Q6(num)
as 
select count(*) 
from (select Q6_Intl_man_2.unswid from Q6_Intl_man_2
except select Q6_eng_3.unswid from Q6_eng_3)as num; 
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q7:
create or replace view Q7_data_mark(term,year,mark,name)
as select sem.term,sem.year,ce.mark,su.name from courses co
	join course_enrolments ce on co.id = ce.course
	join semesters sem on sem.id = co.semester
	join subjects su on su.id = co.subject
where su.name = 'Database Systems' 
and ce.mark is not null
group by sem.term,sem.year,ce.mark,su.name;

create or replace view Q7(year, term, average_mark)
as select Q7_data_mark.year,Q7_data_mark.term,avg(Q7_data_mark.mark)::numeric(4,2) as average_mark
from Q7_data_mark
where Q7_data_mark.mark is not null
group by Q7_data_mark.year ,Q7_data_mark.term
order by Q7_data_mark.year; 
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q8: 
create or replace view Q8(zid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q9:
create or replace view Q9_BSc(unswid,name,abbrev)
as select distinct p1.unswid,p1.name,pd.abbrev from people p1
	join program_enrolments pe on p1.id = pe.student
	join program_degrees pd on pd.program = pe.program
where pd.abbrev = 'BSc';


create or replace view Q9_2010_S2(unswid,name,year,term)
as select distinct Q9_BSc.unswid,Q9_BSc.name,sem.year,sem.term from Q9_BSc
	join people p1 on p1.unswid = Q9_BSc.unswid
	join course_enrolments ce on ce.student = p1.id
	join courses co on co.id = ce.course
	join semesters sem on sem.id = co.semester
	join program_enrolments pe on pe.student = ce.student
	join program_degrees pd on pd.program = pe.program
where sem.year = 2010 and sem.term = 'S2'
and pd.abbrev = 'BSc' and ce.mark >= 50; 

create or replace view Q9_ave_mark(unswid,name,program,ave,year)
as select distinct p1.unswid,p1.name,pe.program,avg(ce.mark)::numeric(4,2) as ave,sem.year from Q9_2010_S2
	join people p1 on p1.unswid = Q9_2010_S2.unswid
	join course_enrolments ce on ce.student = p1.id 
	join courses co on co.id = ce.course
	join program_enrolments pe on pe.student = ce.student
	join semesters sem on sem.id = co.semester
where sem.year < 2011 and ce.mark >= 50
group by p1.unswid, p1.name, pe.program,sem.year;

create or replace view Q9_mark_80(unswid,name)
as select distinct Q9_2010_S2.unswid,Q9_2010_S2.name from Q9_2010_S2
intersect
select distinct Q9_ave_mark.unswid,Q9_ave_mark.name
from Q9_ave_mark 
where Q9_ave_mark.ave >= 80;

create or replace view Q9_sumUoc(unswid,id,name,sumUoc)
as select distinct p1.unswid,p1.id,p1.name,sum(sub.uoc)as sumUoc from Q9_mark_80
	join people p1 on p1.unswid = Q9_mark_80.unswid
	join course_enrolments ce on ce.student = p1.id 
	join courses co on co.id = ce.course
	join semesters sem on sem.id = co.semester
	join subjects sub on sub.id = co.subject
where sem.year < 2011 and ce.mark >= 50
group by p1.unswid,p1.id,p1.name;

create or replace view Q9_Uoc(unswid,name,uoc,sumUoc)
as select distinct Q9_sumUoc.unswid,Q9_sumUoc.name,pr.uoc,Q9_sumUoc.sumUoc from Q9_sumUoc
	join people p1 on p1.unswid = Q9_sumUoc.unswid
	join course_enrolments ce on ce.student = p1.id
	join program_enrolments pe on pe.student = ce.student
	join programs pr on pr.id = pe.program;

create or replace view Q9(unswid, name)
as select Q9_Uoc.unswid as unswid,Q9_Uoc.name as name
from Q9_Uoc 
where Q9_Uoc.uoc <= Q9_Uoc.sumUoc;
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q10:
create or replace view Q10_lec_1(unswid, longname, description)
as select distinct ro.unswid, ro.longname,rt.description from rooms ro 
	join room_types rt on ro.rtype = rt.id
WHERE rt.description = 'Lecture Theatre';

create or replace view Q10_2011_s1_2(unswid, longname,num,description)
as select distinct ro.unswid,ro.longname,cl.id,rt.description from rooms ro 
	join classes cl on cl.room = ro.id 
	join courses co on co.id = cl.course
	join room_types rt on ro.rtype =  rt.id 
	join semesters sem on sem.id = co.semester
where rt.description = 'Lecture Theatre'
AND sem.year = 2011
AND sem.term = 'S1';

create or replace view Q10_count_3(unswid, longname, num)
as
select Q10_2011_s1_2.unswid, Q10_2011_s1_2.longname, count(num) as num from Q10_2011_s1_2
group by Q10_2011_s1_2.unswid, Q10_2011_s1_2.longname
order by num desc;

create or replace view Q10_0_4(unswid, longname, num)
as select Q10_lec_1.unswid, Q10_lec_1.longname ,Cast(0 as decimal) as num
from Q10_lec_1
except select Q10_count_3.unswid, Q10_count_3.longname, Cast(0 as decimal) as num
from Q10_count_3;

create or replace view Q10_link_5(unswid, longname, num)
as
select Q10_count_3.unswid, Q10_count_3.longname, Q10_count_3.num from Q10_count_3,Q10_0_4
union select Q10_0_4.unswid, Q10_0_4.longname, Q10_0_4.num from Q10_0_4
order by num desc;

create or replace view Q10(unswid, longname, num, rank)
as select Q10_link_5.unswid, Q10_link_5.longname, Q10_link_5.num, rank()over(order by Q10_link_5.num desc) as rank
from Q10_link_5;
--... SQL statements, possibly using other views/functions defined by you ...
;

