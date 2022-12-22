select e.name, hw.product, t.task, l.weight from skills_hw s inner join employees e on s.employee=e.id inner join hardware hw on s.product=hw.id inner join tasks_hw t on s.task=t.id inner join levels l on s.level=l.id;

select e.name, sw.product, t.task, l.weight from skills_sw s inner join employees e on s.employee=e.id inner join software sw on s.product=sw.id inner join tasks_sw t on s.task=t.id inner join levels l on s.level=l.id;

select e.name, pr.process, l.weight from skills_pr s inner join employees e on s.employee=e.id inner join processes pr on s.process=pr.id inner join levels l on s.level=l.id;

