<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:local="local">

<xsl:output method="text" />

<xsl:variable name="true-values-array">
	<local:item>true</local:item>
	<local:item>sand</local:item>
	<local:item>vero</local:item>
	<local:item>wahr</local:item>
	<local:item>vrai</local:item>
	<local:item>yes</local:item>
</xsl:variable>
<xsl:param name="true-values" select="document('')/*/xsl:variable[@name='true-values-array']/*" />

<xsl:variable name="false-values-array">
	<local:item>false</local:item>
	<local:item>falsk</local:item>
	<local:item>falskt</local:item>
	<local:item>falso</local:item>
	<local:item>falsch</local:item>
	<local:item>faux</local:item>
	<local:item>no</local:item>
</xsl:variable>
<xsl:param name="false-values" select="document('')/*/xsl:variable[@name='false-values-array']/*" />

<xsl:template name="boolean">
  <xsl:param name="value"/>

  <xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
  <xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>

  <xsl:choose>
    <xsl:when test="count($true-values[. = translate($value,$ucletters,$lcletters)]) > 0">1</xsl:when>
    <xsl:when test="count($false-values[. = translate($value,$ucletters,$lcletters)]) > 0">0</xsl:when>
    <xsl:when test="$value = 'true' or $value = 1">1</xsl:when>
    <xsl:when test="$value = 'false' or $value = 0">0</xsl:when>
    <xsl:otherwise>NULL</xsl:otherwise>
  </xsl:choose><!--, <xsl:call-template name="string"><xsl:with-param name="value" select="$value"/></xsl:call-template>-->
</xsl:template>

<!-- Could also check for commas -->
<!-- Numbers have two columns in the database. One for the numeric value and one for
     the textual presentation -->
<xsl:template name="number">
  <xsl:param name="value"/>
  <xsl:choose>
    <xsl:when test="$value != '' and string(number($value)) != 'NaN'"><xsl:value-of select="$value"/></xsl:when>
    <xsl:otherwise>NULL</xsl:otherwise>
  </xsl:choose>, <xsl:call-template name="string"><xsl:with-param name="value" select="$value"/></xsl:call-template>
</xsl:template>

<xsl:template name="string">
  <xsl:param name="value"/>
  <xsl:choose>
    <xsl:when test="$value != ''">
      <xsl:text>'</xsl:text>
        <xsl:call-template name="globalReplace">
          <xsl:with-param name="outputString" select='$value'/>
        </xsl:call-template>
      <xsl:text>'</xsl:text></xsl:when>
    <xsl:otherwise>NULL</xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- Fixes quotes in database input strings -->
<xsl:template name="globalReplace">
  <xsl:param name="outputString"/>
  <xsl:choose>
    <xsl:when test='contains($outputString,"&apos;")'>
      <xsl:value-of select='concat(substring-before($outputString,"&apos;"),"&apos;&apos;")'/>
      <xsl:call-template name="globalReplace">
        <xsl:with-param name="outputString" select='substring-after($outputString,"&apos;")'/>
      </xsl:call-template>
    </xsl:when>
    <xsl:when test='contains($outputString,"\")'>
      <xsl:value-of select='concat(substring-before($outputString,"\"),"\\;")'/>
      <xsl:call-template name="globalReplace">
        <xsl:with-param name="outputString" select='substring-after($outputString,"\\")'/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="normalize-space($outputString)"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- format datetime -->
<xsl:template name="datetime">
  <xsl:param name="value"/>
  
  <xsl:choose>
    <xsl:when test="normalize-space($value) = '' or normalize-space($value) = &quot;''&quot;">NULL</xsl:when>
    <xsl:otherwise><xsl:text>'</xsl:text>
		<xsl:value-of select="translate($value, 'TZ', ' ')"/>
      <xsl:text>'</xsl:text></xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
