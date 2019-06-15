/**
 * Created by danielecarnovale on 12/01/17.
 */
(function($){
    $.fn.extend({
        tableExport: function(options) {
            var defaults = {
                separator: ',',
                ignoreColumn: [],
                tableName:'yourTableName',
                type:'csv',
                pdfFontSize:14,
                pdfLeftMargin:20,
                escape:'true',
                htmlContent:'false',
                consoleLog:'false'
            };

            var options = $.extend(defaults, options);
            var el = this;

            if(defaults.type == 'excel' ){
                //console.log($(this).html());
                var excel="<table>";
                // Header
                $(el).find('thead').find('tr').each(function() {
                    excel += "<tr>";
                    $(this).filter(':visible').find('th').each(function(index,data) {
                        if ($(this).css('display') != 'none'){
                            if(defaults.ignoreColumn.indexOf(index) == -1){
                                excel += "<td>" + parseString($(this))+ "</td>";
                            }
                        }
                    });
                    excel += '</tr>';

                });


                // Row Vs Column
                var rowCount=1;
                $(el).find('tbody').find('tr').each(function() {
                    excel += "<tr>";
                    var colCount=0;
                    $(this).filter(':visible').find('td').each(function(index,data) {
                        if ($(this).css('display') != 'none'){
                            if(defaults.ignoreColumn.indexOf(index) == -1){
                                excel += "<td>"+parseString($(this))+"</td>";
                            }
                        }
                        colCount++;
                    });
                    rowCount++;
                    excel += '</tr>';
                });
                excel += '</table>'

                if(defaults.consoleLog == 'true'){
                    console.log(excel);
                }

                var excelFile = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:x='urn:schemas-microsoft-com:office:"+defaults.type+"' xmlns='http://www.w3.org/TR/REC-html40'>";
                excelFile += "<head>";
                excelFile += "<!--[if gte mso 9]>";
                excelFile += "<xml>";
                excelFile += "<x:ExcelWorkbook>";
                excelFile += "<x:ExcelWorksheets>";
                excelFile += "<x:ExcelWorksheet>";
                excelFile += "<x:Name>";
                excelFile += "{worksheet}";
                excelFile += "</x:Name>";
                excelFile += "<x:WorksheetOptions>";
                excelFile += "<x:DisplayGridlines/>";
                excelFile += "</x:WorksheetOptions>";
                excelFile += "</x:ExcelWorksheet>";
                excelFile += "</x:ExcelWorksheets>";
                excelFile += "</x:ExcelWorkbook>";
                excelFile += "</xml>";
                excelFile += "<![endif]-->";
                excelFile += "</head>";
                excelFile += "<body>";
                excelFile += excel;
                excelFile += "</body>";
                excelFile += "</html>";


                var uri = 'data:application/vnd.ms-excel;base64,';

                var format = function(s, c) {
                    return s.replace(/{(\w+)}/g, function(m, p) {
                        return c[p];
                    })
                };

                htmls = "La tua Tabella html"

                var ctx = {
                    worksheet : 'Worksheet',
                    table : htmls
                }


                var link = document.createElement("a");
                link.download = "export.xls";
                link.href = uri + window.btoa(unescape(encodeURIComponent(format(excelFile, ctx))));
                link.click();



            }else {

                alert('Tipo Input Errato ');

            }


            function parseString(data){

                if(defaults.htmlContent == 'true'){
                    content_data = data.html().trim();
                }else{
                    content_data = data.text().trim();
                }

                if(defaults.escape == 'true'){
                    content_data = escape(content_data);
                }



                return content_data;
            }

        }
    });
})(jQuery);
