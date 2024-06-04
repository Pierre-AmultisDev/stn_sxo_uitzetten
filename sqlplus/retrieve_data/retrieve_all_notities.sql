select distinct

 CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	WHEN dz1.hoofdzaak_id is not NULL
      THEN dz1.hoofdzaak_id -- dit is een deelzaak kies hoofdzaak id
      ELSE z.id -- dit is geen deelzaak kies het eigen zaak id
   END hoofdzaakid

,  z.aanvraagnummer_string as squitxo_zaaknummer

,  z.extern_zaaknummer as extern_zaaknummer

,  z.globale_locatie_aanduiding as globale_locatie

,  z.omschrijving as omschrijving

,  n.onderwerp as notitie_onderwerp
,  n.tekst as notitie_tekst
,  n.medewerker as notitie_opsteller
,  n.datum as notitie_datum 

from 
   zaak z
   left join deelzaak dz1 on z.id=dz1.id
   left join deelzaak dz2 on z.id=dz2.hoofdzaak_id
   left join vw_g_notities n on z.id = n.zaak_id

where 0=0
AND (n.onderwerp is not null OR n.tekst is not null OR n.medewerker is not null OR n.datum is not null)

order by 
   z.aanvraagnummer_string
