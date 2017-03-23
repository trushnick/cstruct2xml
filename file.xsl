<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="xml" encoding="windows-1251"/>

    <xsl:template match="file">
        <pmodule isDisplay="1" displayName="" comment="" shortName="" idName="">
            <xsl:attribute name="displayName"><xsl:value-of select="@name"/></xsl:attribute>
            <xsl:attribute name="shortName"><xsl:value-of select="@name"/></xsl:attribute>
            <xsl:attribute name="idName"><xsl:value-of select="@name"/></xsl:attribute>
            <xsl:for-each select="structure">
                <sio isDisplay="1" displayName="" comment="" shortName="" idName="">
                    <xsl:attribute name="displayName"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="comment"><xsl:value-of select="description"/></xsl:attribute>
                    <xsl:attribute name="shortName"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="idName"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:for-each select="variables/*">
                        <xsl:if test="local-name() = 'variable'">
                            <xsl:call-template name="var"/>
                        </xsl:if>
                        <xsl:if test="local-name() = 'structure'">
                            <xsl:call-template name="struct"/>
                        </xsl:if>
                    </xsl:for-each>
                </sio>
            </xsl:for-each>
        </pmodule>
    </xsl:template>

    <xsl:template name="struct">
        <struct isDisplay="1" howElements="" comment="" displayName="" shortName="" idName="" isFieldBit="0" numStartBits="0" numEndBits="0">
            <xsl:attribute name="displayName"><xsl:value-of select="name"/></xsl:attribute>
            <xsl:attribute name="howElements"><xsl:value-of select="array_size"/></xsl:attribute>
            <xsl:attribute name="comment"><xsl:value-of select="description"/></xsl:attribute>
            <xsl:attribute name="shortName"><xsl:value-of select="name"/></xsl:attribute>
            <xsl:attribute name="idName"><xsl:value-of select="name"/></xsl:attribute>
            <xsl:for-each select="variables/*">
                <xsl:if test="local-name() = 'variable'">
                    <xsl:call-template name="var"/>
                </xsl:if>
                <xsl:if test="local-name() = 'structure'">
                    <xsl:call-template name="struct"/>
                </xsl:if>
            </xsl:for-each>
        </struct>
    </xsl:template>

    <xsl:template name="var">
        <param isDisplay="1" displayName="" comment="" howElements="" acc="3" type="" messure="" idName="">
            <xsl:attribute name="displayName"><xsl:value-of select="name"/></xsl:attribute>
            <xsl:attribute name="comment"><xsl:value-of select="description"/></xsl:attribute>
            <xsl:attribute name="howElements"><xsl:value-of select="array_size"/></xsl:attribute>
            <xsl:attribute name="type"><xsl:value-of select="type"/></xsl:attribute>
            <xsl:attribute name="idName"><xsl:value-of select="name"/></xsl:attribute>
        </param>
    </xsl:template>

</xsl:stylesheet>
