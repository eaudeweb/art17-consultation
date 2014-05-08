<!DOCTYPE xsl:stylesheet [
    <!ENTITY q "'" >
]>
<!-- ¥ -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="common.xsl"/>

<xsl:output method="text" />

<xsl:param name="dataset"/>
<xsl:param name="role"/>

<xsl:template match="regional">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="species_reports">
    <xsl:text>
    SET NAMES utf8;
    </xsl:text>
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="species_report">
    <xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
	<!--<xsl:text>INSERT INTO data_species VALUES (</xsl:text>
    <xsl:call-template name="string"><xsl:with-param name="value" select="country"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="speciescode"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="speciesname"/></xsl:call-template>,
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(country), normalize-space(speciescode), $s_pos)"/></xsl:call-template>),
    <xsl:call-template name="string"><xsl:with-param name="value" select="/species_reports/@xml:lang"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="$envelopeurl"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="$filename"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="alternative_speciesname"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="common_speciesname"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="distribution_map"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="sensitive_species"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="distribution_method"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="distribution_date"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="additional_distribution_map"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="range_map"/></xsl:call-template>,
    <xsl:call-template name="datetime"><xsl:with-param name="value" select="$uploadtime"/></xsl:call-template>,
    <xsl:call-template name="datetime"><xsl:with-param name="value" select="$accepttime"/></xsl:call-template><xsl:text>);
</xsl:text>
    -->
    <xsl:apply-templates/>

</xsl:template>

<!-- The unique key is the country code, species code and biogeographical region -->
<xsl:template match="region">
	<xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
	<xsl:variable name="sr_pos">[<xsl:number count="region" format="1"/>]</xsl:variable>
    <xsl:text>UPDATE data_species_regions SET
    </xsl:text>
    <xsl:text>rsurface_area=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_surface_area"/></xsl:call-template>, -- range_surface_area
    <xsl:text>range_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_method"/></xsl:call-template>,
    <xsl:text>range_trend_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_period"/></xsl:call-template>,
    <xsl:text>range_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend"/></xsl:call-template>,
    <xsl:text>range_trend_mag_min=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_magnitude_min"/></xsl:call-template>, -- range_trend_mag_min
    <xsl:text>range_trend_mag_max=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_magnitude_max"/></xsl:call-template>, -- range_trend_mag_max
    <xsl:text>range_trend_long_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_long_period"/></xsl:call-template>,
    <xsl:text>range_trend_long=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_long"/></xsl:call-template>,
    <xsl:text>range_trend_long_mag_min=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_long_magnitude_min"/></xsl:call-template>,
    <xsl:text>range_trend_long_mag_max=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="range_trend_long_magnitude_max"/></xsl:call-template>,
    <xsl:text>comp_favourable_range=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_range"/></xsl:call-template>,
    <xsl:text>comp_favourable_range_op=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_range_op"/></xsl:call-template>,
    <xsl:text>comp_favourable_range_x=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="complementary_favourable_range_unknown"/></xsl:call-template>,
    <xsl:text>comp_favourable_range_met=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_range_method"/></xsl:call-template>,
    <xsl:text>r_reasons_for_change_a=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="range_reasons_for_change_a"/></xsl:call-template>,
    <xsl:text>r_reasons_for_change_b=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="range_reasons_for_change_b"/></xsl:call-template>,
    <xsl:text>r_reasons_for_change_c=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="range_reasons_for_change_c"/></xsl:call-template>,
    <xsl:text>pop_size_unit=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_size_unit"/></xsl:call-template>, -- population_size_unit
    <xsl:text>pop_minimum_size=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_minimum_size"/></xsl:call-template>,
    <xsl:text>pop_maximum_size=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_maximum_size"/></xsl:call-template>,
    <xsl:text>pop_alt_size_unit=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_alt_size_unit"/></xsl:call-template>,
    <xsl:text>pop_alt_minimum_size=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_alt_minimum_size"/></xsl:call-template>,
    <xsl:text>pop_alt_maximum_size=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_alt_maximum_size"/></xsl:call-template>,
    <xsl:text>pop_additional_locality=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_additional_locality"/></xsl:call-template>, -- population_additional_locality
    <xsl:text>pop_additional_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_additional_method"/></xsl:call-template>,
    <xsl:text>pop_additional_problems=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_additional_problems"/></xsl:call-template>,
    <xsl:text>pop_date=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_date"/></xsl:call-template>, -- pop_date
    <xsl:text>pop_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_method"/></xsl:call-template>,
    <xsl:text>pop_trend_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_period"/></xsl:call-template>,
    <xsl:text>pop_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend"/></xsl:call-template>,
    <xsl:text>pop_trend_mag_min=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_magnitude_min"/></xsl:call-template>, -- pop_trend_mag_min
    <xsl:text>pop_trend_mag_max=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_magnitude_max"/></xsl:call-template>,
    <xsl:text>pop_trend_magnitude_ci=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_magnitude_ci"/></xsl:call-template>,
    <xsl:text>pop_trend_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_method"/></xsl:call-template>,
    <xsl:text>pop_trend_long_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long_period"/></xsl:call-template>,
    <xsl:text>population_trend_long=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long"/></xsl:call-template>, -- pop_trend_long
    <xsl:text>pop_trend_long_mag_min=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long_magnitude_min"/></xsl:call-template>,
    <xsl:text>pop_trend_long_mag_max=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long_magnitude_max"/></xsl:call-template>,
    <xsl:text>pop_trend_long_mag_ci=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long_magnitude_ci"/></xsl:call-template>,
    <xsl:text>pop_trend_long_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="population_trend_long_method"/></xsl:call-template>,
    <xsl:text>comp_favourable_pop=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_population"/></xsl:call-template>, -- comp_favourable_population
    <xsl:text>comp_favourable_pop_op=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_population_op"/></xsl:call-template>,
    <xsl:text>comp_favourable_pop_x=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="complementary_favourable_population_unknown"/></xsl:call-template>,
    <xsl:text>comp_favourable_pop_met=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="complementary_favourable_population_method"/></xsl:call-template>,
    <xsl:text>pop_reasons_for_change_a=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="population_reasons_for_change_a"/></xsl:call-template>,
    <xsl:text>pop_reasons_for_change_b=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="population_reasons_for_change_b"/></xsl:call-template>,
    <xsl:text>pop_reasons_for_change_c=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="population_reasons_for_change_c"/></xsl:call-template>,
    <xsl:text>habitat_surface_area=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_surface_area"/></xsl:call-template>, -- habitat_surface_area
    <xsl:text>habitat_date=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_date"/></xsl:call-template>,
    <xsl:text>habitat_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_method"/></xsl:call-template>,
    <xsl:text>habitat_quality=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_quality"/></xsl:call-template>,
    <xsl:text>habitat_quality_explanation=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_quality_explanation"/></xsl:call-template>,
    <xsl:text>habitat_trend_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_trend_period"/></xsl:call-template>,
    <xsl:text>habitat_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_trend"/></xsl:call-template>, -- habitat_trend
    <xsl:text>habitat_trend_long_period=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_trend_long_period"/></xsl:call-template>,
    <xsl:text>habitat_trend_long=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_trend_long"/></xsl:call-template>,
    <xsl:text>habitat_area_suitable=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="habitat_area_suitable"/></xsl:call-template>,
    <xsl:text>habitat_reasons_for_change__61=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="habitat_reasons_for_change_a"/></xsl:call-template>,
    <xsl:text>habitat_reasons_for_change__62=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="habitat_reasons_for_change_b"/></xsl:call-template>,
    <xsl:text>habitat_reasons_for_change__63=</xsl:text><xsl:call-template name="boolean"><xsl:with-param name="value" select="habitat_reasons_for_change_c"/></xsl:call-template>,
    <xsl:text>pressures_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="pressures_method"/></xsl:call-template>, -- pressures_method
    <xsl:text>threats_method=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="threats_method"/></xsl:call-template>,
    <xsl:text>justification=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="justification"/></xsl:call-template>,
    <xsl:text>other_relevant_information=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="other_relevant_information"/></xsl:call-template>,
    <xsl:text>transboundary_assessment=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="transboundary_assessment"/></xsl:call-template>,
    <xsl:text>conclusion_range=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_range"/></xsl:call-template>, -- conclusion_range
    <xsl:text>conclusion_range_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_range_trend"/></xsl:call-template>,
    <xsl:text>conclusion_population=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_population"/></xsl:call-template>,
    <xsl:text>conclusion_population_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_population_trend"/></xsl:call-template>,
    <xsl:text>conclusion_habitat=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_habitat"/></xsl:call-template>,
    <xsl:text>conclusion_habitat_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_habitat_trend"/></xsl:call-template>,
    <xsl:text>conclusion_future=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_future"/></xsl:call-template>,
    <xsl:text>conclusion_future_trends=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_future_trends"/></xsl:call-template>,
    <xsl:text>conclusion_assessment=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_assessment"/></xsl:call-template>, -- conclusion_assessment
    <xsl:text>conclusion_assessment_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="conclusion_assessment_trend"/></xsl:call-template>,
    <xsl:text>natura2000_population_unit=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="natura2000_population_unit"/></xsl:call-template>,
    <xsl:text>natura2000_population_min=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="natura2000_population_min"/></xsl:call-template>,
    <xsl:text>natura2000_population_max=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="natura2000_population_max"/></xsl:call-template>,
    <xsl:text>natura2000_population_metho_82=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="natura2000_population_method"/></xsl:call-template>, -- natura2000_population_method
    <xsl:text>natura2000_population_trend=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="natura2000_population_trend"/></xsl:call-template><xsl:text>

    WHERE sr_species_id=(SELECT objectid FROM data_species WHERE speciescode=</xsl:text>
    <xsl:call-template name="string"><xsl:with-param name="value" select="../../speciescode"></xsl:with-param></xsl:call-template>
    <xsl:text>)
    AND region=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="code"></xsl:with-param></xsl:call-template><xsl:text>
    AND cons_dataset_id=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="$dataset"></xsl:with-param></xsl:call-template><xsl:text>
    AND cons_role=</xsl:text><xsl:call-template name="string"><xsl:with-param name="value" select="$role"></xsl:with-param></xsl:call-template>
    <xsl:text>;
</xsl:text>
    <xsl:apply-templates select="pressures/pressure"/>
    <xsl:apply-templates select="threats/threat"/>
    <xsl:apply-templates select="measures/measure"/>
</xsl:template>


<xsl:template match="pressures/pressure">
    	<xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
	    <xsl:variable name="sr_pos">[<xsl:number count="region" format="1"/>]</xsl:variable>
	    <xsl:variable name="p_pos">[p<xsl:number count="pressure" format="1"/>]</xsl:variable>

    <!--
    insert into data_pressures_threats
      (objectid,
      pressure_sr_id,
      pressure,
      ranking,
      type)
      WITH DATA AS
      (
        select objectid obj, 'test' pressure,
        'H' ranking,
        'p' tip
        'random' globalid,
         from data_species_regions
        where sr_species_id=(select objectid from data_species
                                where speciescode=1014) and cons_dataset_id=3 and region='CON' and cons_role='assessment'
      )
      select R667.nextval, obj, pressure, ranking, tip, globalid from data;
    -->
    <!--<xsl:text>INSERT INTO data_pressures_threats VALUES (</xsl:text>
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../country), normalize-space(../../../../speciescode), $s_pos, normalize-space(../../code), $sr_pos, normalize-space(code), $p_pos)"/></xsl:call-template>),
	NULL,
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../country), normalize-space(../../../../speciescode), $s_pos, normalize-space(../../code), $sr_pos)"/></xsl:call-template>),
    <xsl:call-template name="string"><xsl:with-param name="value" select="normalize-space(code)"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="ranking"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="'p'"/></xsl:call-template>
    <xsl:text>);
</xsl:text>-->
            <xsl:apply-templates select="pollution_qualifiers/pollution_qualifier"/>
</xsl:template>




<xsl:template match="threats/threat">
    	<xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
	    <xsl:variable name="sr_pos">[<xsl:number count="region" format="1"/>]</xsl:variable>
	    <xsl:variable name="t_pos">[t<xsl:number count="threat" format="1"/>]</xsl:variable>
    <!--<xsl:text>INSERT INTO data_pressures_threats VALUES (</xsl:text>
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../country), normalize-space(../../../../speciescode), $s_pos, normalize-space(../../code), $sr_pos, normalize-space(code), $t_pos)"/></xsl:call-template>),
	NULL,
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../country), normalize-space(../../../../speciescode), $s_pos, normalize-space(../../code), $sr_pos)"/></xsl:call-template>),
    <xsl:call-template name="string"><xsl:with-param name="value" select="normalize-space(code)"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="ranking"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="'t'"/></xsl:call-template>
    <xsl:text>);
</xsl:text>-->
            <xsl:apply-templates select="pollution_qualifiers/pollution_qualifier"/>
</xsl:template>


<xsl:template match="pollution_qualifiers/pollution_qualifier">
    	<xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
		<xsl:variable name="parent"><xsl:value-of select="name(parent::*/parent::*)"/></xsl:variable>
	    <xsl:variable name="sr_pos">[<xsl:number count="region" format="1"/>]</xsl:variable>
	    <xsl:variable name="tp_pos">[<xsl:value-of select="substring($parent,1,1)"/><xsl:choose><xsl:when test="$parent='threat'"><xsl:number count="threat" format="1"/></xsl:when><xsl:otherwise><xsl:number count="pressure" format="1"/></xsl:otherwise></xsl:choose>]</xsl:variable>
		<!-- TODO pol ID -->
    <!--<xsl:text>INSERT INTO data_pressures_threats_pol VALUES (</xsl:text>
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../../../country), normalize-space(../../../../../../speciescode), $s_pos, normalize-space(../../../../code), $sr_pos, normalize-space(../../code), $tp_pos)"/></xsl:call-template>),
    <xsl:call-template name="string"><xsl:with-param name="value" select="normalize-space(../../code)"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="normalize-space(code)"/></xsl:call-template>
    <xsl:text>);
</xsl:text>-->
</xsl:template>



<xsl:template match="measures/measure">
    	<xsl:variable name="s_pos">[<xsl:number count="species_report" format="1"/>]</xsl:variable>
	    <xsl:variable name="sr_pos">[<xsl:number count="region" format="1"/>]</xsl:variable>
	    <xsl:variable name="m_pos">[<xsl:number count="measure" format="1"/>]</xsl:variable>
    <!--<xsl:text>INSERT INTO data_measures VALUES (</xsl:text>
	NULL,
    MD5(<xsl:call-template name="string"><xsl:with-param name="value" select="concat($envelopeurl, $filename, normalize-space(../../../../country), normalize-space(../../../../speciescode), $s_pos, normalize-space(../../code), $sr_pos)"/></xsl:call-template>),
    <xsl:call-template name="string"><xsl:with-param name="value" select="normalize-space(code)"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="type_legal"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="type_administrative"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="type_contractual"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="type_recurrent"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="type_oneoff"/></xsl:call-template>,
    <xsl:call-template name="string"><xsl:with-param name="value" select="ranking"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="location_inside"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="location_outside"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="location_both"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_maintain"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_enhance"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_longterm"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_noeffect"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_unknown"/></xsl:call-template>,
    <xsl:call-template name="boolean"><xsl:with-param name="value" select="broad_evaluation_notevaluated"/></xsl:call-template>
    <xsl:text>);
</xsl:text>-->
</xsl:template>

<xsl:template match="text()"/>

</xsl:stylesheet>
