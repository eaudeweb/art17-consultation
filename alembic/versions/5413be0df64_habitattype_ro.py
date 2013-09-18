# encoding: utf-8

revision = '5413be0df64'
down_revision = '363a0d66f02f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_habitattype_codes',
        sa.Column('hd_name_ro', sa.UnicodeText, nullable=True))

    lu_habitattype_codes = table('lu_habitattype_codes',
        column('code', sa.String),
        column('hd_name_ro', sa.UnicodeText))

    for code, name_ro in DATA:
        op.execute(
            lu_habitattype_codes.update()
                                .where(lu_habitattype_codes.c.code == code)
                                .values({'hd_name_ro': name_ro}))


def downgrade():
    op.drop_column('lu_habitattype_codes', 'hd_name_ro')


DATA = [
    ('1110', u"Bancuri de nisip submerse de mică adâncime"),
    ('1130', u"Estuare și guri de vărsare ale marilor râuri și fluvii"),
    ('1140', u"Suprafețe de nisip și mâl descoperite la maree joasă"),
    ('1150', u"Lagune costiere"),
    ('1160', u"Brațe de mare și golfuri mai puțin adânci"),
    ('1170', u"Recifi"),
    ('1180', u"Structuri submarine create de emisiile de gaze"),
    ('1210', u"Vegetație anuală de-a lungul liniei țărmului"),
    ('1310', u"Comunități cu Salicornia și alte specii anuale care "
             u"colonizează terenurile umede și nisipoase"),
    ('1410', u"Pajiști halofile de tip mediteranean (Juncetalia maritimi)"),
    ('1530', u"Pajiști și mlaștini halofile panonice și ponto-sarmatice"),
    ('2110', u"Dune mobile embrionare (în formare)"),
    ('2130', u"Dune fixate cu vegetație herbacee perenă (dune gri)"),
    ('2160', u"Dune cu Hippophaë rhamnoides"),
    ('2190', u"Depresiuni umede interdunale"),
    ('2330', u"Dune cu Corynephorus și Agrostis"),
    ('2340', u"Dune panonice"),
    ('3130', u"Ape stătătoare oligotrofice până la mezotrofice cu vegetație "
             u"din Littorelletea uniflorae și/sau Isoëto-Nanojuncetea"),
    ('3140', u"Ape puternic oligo-mezotrofice cu vegetație bentonică de "
             u"specii de Chara"),
    ('3150', u"Lacuri naturale eutrofice cu vegetație tip Magnopotamion "
             u"sau Hydrocharition"),
    ('3160', u"Lacuri distrofice și iazuri"),
    ('31A0', u"Ape termale din Transilvania acoperite cu lotus (drețe)"),
    ('3220', u"Vegetație herbacee de pe malurile râurilor montane"),
    ('3230', u"Vegetație lemnoasă cu Myricaria germanica de-a lungul "
             u"râurilor montane"),
    ('3240', u"Vegetație lemnoasă cu Salix elaeagnos de-a lungul râurilor "
             u"montane"),
    ('3260', u"Cursuri de apă din zona de câmpie până în etajul montan, cu "
             u"vegetație din Ranunculion fluitantis și "
             u"Callitricho-Batrachion"),
    ('3270', u"Râuri cu maluri nămoloase cu vegetație din Chenopodion "
             u"rubri și Bidention"),
    ('4030', u"Tufărișuri uscate europene"),
    ('4060', u"Tufărișuri alpine și boreale"),
    ('4070', u"Tufărișuri cu Pinus mugo și Rhododendron myrtifolium"),
    ('4080', u"Tufărișuri cu specii sub-arctice de Salix"),
    ('40A0', u"Tufărișuri subcontinentale peri-panonice"),
    ('40C0', u"Tufărișuri de foioase ponto-sarmatice"),
    ('6110', u"Comunități rupicole calcifile sau pajiști bazifile din "
             u"Alysso-Sedion albi"),
    ('6120', u"Pajiști xerice pe substrate calcaroase"),
    ('6150', u"Pajiști boreale și alpine pe substrate silicioase"),
    ('6170', u"Pajiști calcifile alpine și subalpine"),
    ('6190', u"Pajiști panonice de stâncării (Stipo-Festucetalia "
             u"pallentis)"),
    ('6210', u"Pajiști uscate seminaturale și faciesuri cu tufărișuri pe "
             u"substrate calcaroase (Festuco Brometalia)"),
    ('6230', u"Pajiști montane de Nardus bogate în specii, pe substrate "
             u"silicioase"),
    ('6240', u"Pajiști stepice subpanonice"),
    ('6250', u"Pajiști panonice pe loess"),
    ('6260', u"Pajiști panonice și vest-pontice pe nisipuri"),
    ('62C0', u"Stepe ponto-sarmatice"),
    ('6410', u"Pajiști cu Molinia pe soluri calcaroase, turboase sau "
             u"argiloase (Molinion caeruleae)"),
    ('6420', u"Pajiști mediteraneene umede cu ierburi înalte din "
             u"Molinio-Holoschoenion"),
    ('6430', u"Comunități de lizieră cu ierburi înalte higrofile de la "
             u"câmpie până în etajele montan și alpin"),
    ('6440', u"Pajiști aluviale din Cnidion dubii"),
    ('6510', u"Pajiști de altitudine joasă (Alopecurus pratensis, "
             u"Sanguisorba officinalis)"),
    ('6520', u"Fânețe montane"),
    ('7110', u"Turbării active"),
    ('7120', u"Turbării degradate capabile de regenerare naturală"),
    ('7140', u"Mlaștini turboase de tranziție și turbării oscilante "
             u"(nefixate de substrat)"),
    ('7150', u"Comunități depresionare din Rhynchosporion pe substrate "
             u"turboase"),
    ('7210', u"Mlaștini calcaroase cu Cladium mariscus"),
    ('7220', u"Izvoare petrifiante cu formare de travertin "
             u"(Cratoneurion)"),
    ('7230', u"Mlaștini alcaline"),
    ('7240', u"Formațiuni pioniere alpine din Caricion "
             u"bicoloris-atrofuscae"),
    ('8110', u"Grohotișuri silicioase din etajele montan și alpin "
             u"(Androsacetalia alpinae și Galeopsietalia ladani)"),
    ('8120', u"Grohotișuri calcaroase și de șisturi calcaroase din etajele "
             u"montan și alpin (Thlaspietea rotundifolii)"),
    ('8160', u"Grohotișuri medio-europene calcaroase din etajele colinar "
             u"și montan"),
    ('8210', u"Versanți stâncoși cu vegetație chasmofitică pe roci "
             u"calcaroase"),
    ('8220', u"Versanți stâncoși cu vegetație chasmofitică pe roci "
             u"silicioase"),
    ('8230', u"Comunități pioniere din Sedo-Scleranthion sau din Sedo "
             u"albi-Veronicion dilleni pe stâncării silicioase"),
    ('8310', u"Peșteri în care accesul publicului este interzis"),
    ('8330', u"Pesteri marine total sau partial submerse"),
    ('9110', u"Păduri de fag de tip Luzulo-Fagetum"),
    ('9130', u"Păduri de fag de tip Asperulo-Fagetum"),
    ('9150', u"Păduri medio-europene de fag din Cephalanthero-Fagion"),
    ('9170', u"Pãduri de stejar cu carpen de tip Galio-Carpinetum"),
    ('9180', u"Păduri din Tilio-Acerion pe versanți abrupți, grohotișuri "
             u"și ravene"),
    ('91AA', u"Vegetație forestieră ponto-sarmatică cu stejar pufos"),
    ('91D0', u"Turbării cu vegetație forestieră"),
    ('91E0', u"Păduri aluviale cu Alnus glutinosa și Fraxinus excelsior "
             u"(Alno-Padion, Alnion incanae, Salicion albae)"),
    ('91F0', u"Păduri ripariene mixte cu Quercus robur, Ulmus laevis, "
             u"Fraxinus excelsior sau Fraxinus angustifolia, din "
             u"lungul marilor râuri (Ulmenion minoris)"),
    ('91H0', u"Vegetație forestieră panonică cu Quercus pubescens"),
    ('91I0', u"Vegetație de silvostepă eurosiberiană cu Quercus spp."),
    ('91K0', u"Păduri ilirice de Fagus sylvatica (Aremonio-Fagion)"),
    ('91L0', u"Păduri ilirice de stejar cu carpen (Erythronio-Carpinion)"),
    ('91M0', u"Păduri balcano-panonice de cer și gorun"),
    ('91Q0', u"Păduri relictare cu Pinus sylvestris pe substrate calcaroase"),
    ('91V0', u"Păduri dacice de fag (Symphyto-Fagion)"),
    ('91X0', u"Păduri dobrogene de fag"),
    ('91Y0', u"Păduri dacice de stejar și carpen"),
    ('9260', u"Vegetație forestieră cu Castanea sativa"),
    ('92A0', u"Zăvoaie cu Salix alba și Populus alba"),
    ('92D0', u"Galerii ripariene și tufărișuri (Nerio-Tamaricetea și "
             u"Securinegion tinctoriae)"),
    ('9410', u"Păduri acidofile de Picea abies din regiunea montana "
             u"(Vaccinio-Piceetea)"),
    ('9420', u"Păduri de Larix decidua și/sau Pinus cembra din "
             u"regiunea montană"),
    ('9530', u"Vegetație forestieră sub-mediteraneeană cu endemitul "
             u"Pinus nigra ssp. banatica"),
]
