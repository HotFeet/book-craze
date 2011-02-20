<?xml version="1.0" encoding="ISO-8859-1" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" />

	<xsl:template match="/">
		<books>
			<xsl:apply-templates select="html/body/table/tr[position() &gt; 1]" />
		</books>
	</xsl:template>

	<xsl:template match="tr">
		<book>
			<xsl:attribute name="title">
				<xsl:value-of select="td[1]/text()" />
			</xsl:attribute>
			<xsl:attribute name="isbn">
				<xsl:value-of select="td[4]/text()" />
			</xsl:attribute>
		</book>
	</xsl:template>

	<xsl:template match="text()" />

</xsl:stylesheet>