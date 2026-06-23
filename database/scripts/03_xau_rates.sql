-- ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
USE xau;

insert ignore into Rate (pkfk_uid, pk_dt, priceBceeBuy, priceBceeSell)
select m.uid, d.pk_dt,
round(m.priceBceeBuy*(d.priceBceeBuy+d.priceBceeSell) * mul,2) priceBceeBuy,
round(m.priceBceeSell*(d.priceBceeBuy+d.priceBceeSell) *mul,2)  priceBceeSell
from Rate d,
( select a.uid,
(ar.priceBceeBuy+br.priceBceeBuy)/(ar.priceBceeBuy+br.priceBceeSell+br.priceBceeBuy+ar.priceBceeSell) priceBceeBuy,
(ar.priceBceeSell+br.priceBceeSell)/(ar.priceBceeBuy+br.priceBceeSell+br.priceBceeBuy+ar.priceBceeSell) priceBceeSell
from Xau a
JOIN Rate ar ON a.uid = ar.pkfk_uid
JOIN Rate br ON a.uid = br.pkfk_uid
where a.uid != 308
and ar.pk_dt = '2026-01-13'
and br.pk_dt = '2026-01-17' ) m,
( select ar.pkfk_uid uid,
((ar.priceBceeBuy/br.priceBceeBuy)+(ar.priceBceeSell/br.priceBceeSell)) / 2 mul
from Rate ar, Rate br
where br.pkfk_uid = 308
and ar.pk_dt = '2026-01-13'
and br.pk_dt = '2026-01-17' ) n
where d.pkfk_uid = 308
and d.pk_dt not in ('2026-01-13','2026-01-17')
and m.uid = n.uid
order by d.pk_dt, m.uid
;