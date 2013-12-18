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
                .where(lu_habitattype_codes.c.code == op.inline_literal(code))
                .values({'hd_name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_habitattype_codes', 'hd_name_ro')


DATA = [
    ('1110', u"Bancuri de nisip submerse de mica adancime"),
    ('1130', u"Estuare si guri de varsare ale marilor rauri si fluvii"),
    ('1140', u"Suprafete de nisip si mal descoperite la maree joasa"),
    ('1150', u"Lagune costiere"),
    ('1160', u"Brate de mare si golfuri mai putin adanci"),
    ('1170', u"Recifi"),
    ('1180', u"Structuri submarine create de emisiile de gaze"),
    ('1210', u"Vegetatie anuala de-a lungul liniei tarmului"),
    ('1310', u"Comunitati cu Salicornia si alte specii anuale care "
             u"colonizeaza terenurile umede si nisipoase"),
    ('1410', u"Pajisti halofile de tip mediteranean (Juncetalia maritimi)"),
    ('1530', u"Pajisti si mlastini halofile panonice si ponto-sarmatice"),
    ('2110', u"Dune mobile embrionare (in formare)"),
    ('2130', u"Dune fixate cu vegetatie herbacee perena (dune gri)"),
    ('2160', u"Dune cu Hippophaë rhamnoides"),
    ('2190', u"Depresiuni umede interdunale"),
    ('2330', u"Dune cu Corynephorus si Agrostis"),
    ('2340', u"Dune panonice"),
    ('3130', u"Ape statatoare oligotrofice pana la mezotrofice cu vegetatie "
             u"din Littorelletea uniflorae si/sau Isoëto-Nanojuncetea"),
    ('3140', u"Ape puternic oligo-mezotrofice cu vegetatie bentonica de "
             u"specii de Chara"),
    ('3150', u"Lacuri naturale eutrofice cu vegetatie tip Magnopotamion "
             u"sau Hydrocharition"),
    ('3160', u"Lacuri distrofice si iazuri"),
    ('31A0', u"Ape termale din Transilvania acoperite cu lotus (drete)"),
    ('3220', u"Vegetatie herbacee de pe malurile raurilor montane"),
    ('3230', u"Vegetatie lemnoasa cu Myricaria germanica de-a lungul "
             u"raurilor montane"),
    ('3240', u"Vegetatie lemnoasa cu Salix elaeagnos de-a lungul raurilor "
             u"montane"),
    ('3260', u"Cursuri de apa din zona de campie pana in etajul montan, cu "
             u"vegetatie din Ranunculion fluitantis si "
             u"Callitricho-Batrachion"),
    ('3270', u"Rauri cu maluri namoloase cu vegetatie din Chenopodion "
             u"rubri si Bidention"),
    ('4030', u"Tufarisuri uscate europene"),
    ('4060', u"Tufarisuri alpine si boreale"),
    ('4070', u"Tufarisuri cu Pinus mugo si Rhododendron myrtifolium"),
    ('4080', u"Tufarisuri cu specii sub-arctice de Salix"),
    ('40A0', u"Tufarisuri subcontinentale peri-panonice"),
    ('40C0', u"Tufarisuri de foioase ponto-sarmatice"),
    ('6110', u"Comunitati rupicole calcifile sau pajisti bazifile din "
             u"Alysso-Sedion albi"),
    ('6120', u"Pajisti xerice pe substrate calcaroase"),
    ('6150', u"Pajisti boreale si alpine pe substrate silicioase"),
    ('6170', u"Pajisti calcifile alpine si subalpine"),
    ('6190', u"Pajisti panonice de stancarii (Stipo-Festucetalia "
             u"pallentis)"),
    ('6210', u"Pajisti uscate seminaturale si faciesuri cu tufarisuri pe "
             u"substrate calcaroase (Festuco Brometalia)"),
    ('6230', u"Pajisti montane de Nardus bogate in specii, pe substrate "
             u"silicioase"),
    ('6240', u"Pajisti stepice subpanonice"),
    ('6250', u"Pajisti panonice pe loess"),
    ('6260', u"Pajisti panonice si vest-pontice pe nisipuri"),
    ('62C0', u"Stepe ponto-sarmatice"),
    ('6410', u"Pajisti cu Molinia pe soluri calcaroase, turboase sau "
             u"argiloase (Molinion caeruleae)"),
    ('6420', u"Pajisti mediteraneene umede cu ierburi inalte din "
             u"Molinio-Holoschoenion"),
    ('6430', u"Comunitati de liziera cu ierburi inalte higrofile de la "
             u"campie pana in etajele montan si alpin"),
    ('6440', u"Pajisti aluviale din Cnidion dubii"),
    ('6510', u"Pajisti de altitudine joasa (Alopecurus pratensis, "
             u"Sanguisorba officinalis)"),
    ('6520', u"Fanete montane"),
    ('7110', u"Turbarii active"),
    ('7120', u"Turbarii degradate capabile de regenerare naturala"),
    ('7140', u"Mlastini turboase de tranzitie si turbarii oscilante "
             u"(nefixate de substrat)"),
    ('7150', u"Comunitati depresionare din Rhynchosporion pe substrate "
             u"turboase"),
    ('7210', u"Mlastini calcaroase cu Cladium mariscus"),
    ('7220', u"Izvoare petrifiante cu formare de travertin "
             u"(Cratoneurion)"),
    ('7230', u"Mlastini alcaline"),
    ('7240', u"Formatiuni pioniere alpine din Caricion "
             u"bicoloris-atrofuscae"),
    ('8110', u"Grohotisuri silicioase din etajele montan si alpin "
             u"(Androsacetalia alpinae si Galeopsietalia ladani)"),
    ('8120', u"Grohotisuri calcaroase si de sisturi calcaroase din etajele "
             u"montan si alpin (Thlaspietea rotundifolii)"),
    ('8160', u"Grohotisuri medio-europene calcaroase din etajele colinar "
             u"si montan"),
    ('8210', u"Versanti stancosi cu vegetatie chasmofitica pe roci "
             u"calcaroase"),
    ('8220', u"Versanti stancosi cu vegetatie chasmofitica pe roci "
             u"silicioase"),
    ('8230', u"Comunitati pioniere din Sedo-Scleranthion sau din Sedo "
             u"albi-Veronicion dilleni pe stancarii silicioase"),
    ('8310', u"Pesteri in care accesul publicului este interzis"),
    ('8330', u"Pesteri marine total sau partial submerse"),
    ('9110', u"Paduri de fag de tip Luzulo-Fagetum"),
    ('9130', u"Paduri de fag de tip Asperulo-Fagetum"),
    ('9150', u"Paduri medio-europene de fag din Cephalanthero-Fagion"),
    ('9170', u"Pãduri de stejar cu carpen de tip Galio-Carpinetum"),
    ('9180', u"Paduri din Tilio-Acerion pe versanti abrupti, grohotisuri "
             u"si ravene"),
    ('91AA', u"Vegetatie forestiera ponto-sarmatica cu stejar pufos"),
    ('91D0', u"Turbarii cu vegetatie forestiera"),
    ('91E0', u"Paduri aluviale cu Alnus glutinosa si Fraxinus excelsior "
             u"(Alno-Padion, Alnion incanae, Salicion albae)"),
    ('91F0', u"Paduri ripariene mixte cu Quercus robur, Ulmus laevis, "
             u"Fraxinus excelsior sau Fraxinus angustifolia, din "
             u"lungul marilor rauri (Ulmenion minoris)"),
    ('91H0', u"Vegetatie forestiera panonica cu Quercus pubescens"),
    ('91I0', u"Vegetatie de silvostepa eurosiberiana cu Quercus spp."),
    ('91K0', u"Paduri ilirice de Fagus sylvatica (Aremonio-Fagion)"),
    ('91L0', u"Paduri ilirice de stejar cu carpen (Erythronio-Carpinion)"),
    ('91M0', u"Paduri balcano-panonice de cer si gorun"),
    ('91Q0', u"Paduri relictare cu Pinus sylvestris pe substrate calcaroase"),
    ('91V0', u"Paduri dacice de fag (Symphyto-Fagion)"),
    ('91X0', u"Paduri dobrogene de fag"),
    ('91Y0', u"Paduri dacice de stejar si carpen"),
    ('9260', u"Vegetatie forestiera cu Castanea sativa"),
    ('92A0', u"Zavoaie cu Salix alba si Populus alba"),
    ('92D0', u"Galerii ripariene si tufarisuri (Nerio-Tamaricetea si "
             u"Securinegion tinctoriae)"),
    ('9410', u"Paduri acidofile de Picea abies din regiunea montana "
             u"(Vaccinio-Piceetea)"),
    ('9420', u"Paduri de Larix decidua si/sau Pinus cembra din "
             u"regiunea montana"),
    ('9530', u"Vegetatie forestiera sub-mediteraneeana cu endemitul "
             u"Pinus nigra ssp. banatica"),
]
