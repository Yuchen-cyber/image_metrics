# https://www.reportlab.com/
from reportlab.lib.pagesizes import  landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import  mm
from reportlab.lib.utils import simpleSplit
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

class PDFWriter():
    def __init__(self, filename, id):
        # create a new PDF document
        self.filename = filename
        self.pdf_filename = filename +'/submission_'+ str(id) + '/RESULTS/result_report_pdf.pdf'
        self.pdf = canvas.Canvas(self.pdf_filename, pagesize=landscape(A4))
        self.id = id
        self.line_distance = 20
        self.start_point = A4[0] / 1.2
    def generate_pdf(self):

        self.saliency_page()
        self.pdf.showPage()
        
        self.white_space_page()
        self.pdf.showPage()
        
    
        self.colour_page()
        self.pdf.showPage()
        
        self.text_area_page()
        self.pdf.showPage()
        
        self.reference_page()


        # save the PDF document
        self.pdf.save()
        
    def saliency_page(self):
        # set the font and font size for the text
        self.pdf.setFont("Helvetica-Bold", 24)

        # draw the text in the center of the page
        text = "Saliency"
        self.pdf.drawCentredString(A4[1] / 2, A4[0] / 1.2, text)
        # set the font and font size for the unbold text
        start_point = self.start_point - self.line_distance
        availWidth, availHeight = 250*mm, A4[1]

        style = ParagraphStyle("justifies", alignment=TA_JUSTIFY, fontSize=11, leading=12)
        self.pdf.setFont("Helvetica", 12)
        saliency_description = """Saliency detection is widely used and this metric can predict the human attention map of one image efficiently.
        The brighter areas mean more attention. The graph below is processed by the machine predicting the attention human may percieve. The function to implement this metric is from OpenCV[2].
        If your saliency value is very low, the suggestion would be make the key elements have more constast edges[1].
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(saliency_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
        self.pdf.drawText(textobject)
        image_filename =self.filename + '/submission_' + str(self.id)+ '/out1R.png'
        self.pdf.drawImage(image_filename, x=A4[1] / 6, y=200, width=250, height=150)
        saliency_image_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/saliency.png'
        self.pdf.drawImage(saliency_image_filename, x=A4[1] / 6 + 290, y=200, width=250, height=150)
        saliency_correlation_filename ='submissions/correlations/saliency_similarity.png'
        self.pdf.drawImage(saliency_correlation_filename, x=A4[1] / 6 - 30, y=50, width=300, height=150)
        saliency_result_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/saliency_result.png'
        self.pdf.drawImage(saliency_result_filename, x=A4[1] / 6 + 270, y=50, width=300, height=150)
        
    def white_space_page(self):
        # set the font and font size for the text
        self.pdf.setFont("Helvetica-Bold", 24)

        # draw the text in the center of the page
        text = "White Space Proportion"
        self.pdf.drawCentredString(A4[1] / 2, A4[0] / 1.2, text)
        # set the font and font size for the unbold text
        start_point = self.start_point - self.line_distance
        availWidth, availHeight = 250*mm, A4[1]

        style = ParagraphStyle("justifies", alignment=TA_JUSTIFY, fontSize=11, leading=12)
        self.pdf.setFont("Helvetica", 12)
        white_space_description = """The white space that is not covered by any visual blocks in this image\cite[2]. This metric is to assess the layout of this GUI image and is considered to be negatively related to the quality of the GUI image[2]. The algorithm is to first detect the visual block and then get the uncovered space in the image[2].
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(white_space_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
        self.pdf.drawText(textobject)
        image_filename =self.filename + '/submission_' + str(self.id)+ '/out1R.png'
        self.pdf.drawImage(image_filename, x=A4[1] / 6, y=200,width=250, height=150)
        saliency_image_filename =self.filename + '/submission_'+ str(self.id) + '/RESULTS//left.png'
        self.pdf.drawImage(saliency_image_filename, x=A4[1] / 6 + 290, y = 200, width=250, height=150)
        white_space_correlation_filename ='submissions/correlations/white_space_similarity.png'
        self.pdf.drawImage(white_space_correlation_filename, x=A4[1] / 6 - 30, y=50, width=300, height=150)
        white_space_result_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/white_space_result.png'
        self.pdf.drawImage(white_space_result_filename, x=A4[1] / 6 + 270, y=50, width=300, height=150)
        
        
    def text_area_page(self):
        # set the font and font size for the text
        self.pdf.setFont("Helvetica-Bold", 24)

        # draw the text in the center of the page
        text = "Text Layout"
        self.pdf.drawCentredString(A4[1] / 2, A4[0] / 1.2, text)
        # set the font and font size for the unbold text
        start_point = self.start_point - self.line_distance
        availWidth, availHeight = 250*mm, A4[1]

        style = ParagraphStyle("justifies", alignment=TA_JUSTIFY, fontSize=11, leading=12)
        self.pdf.setFont("Helvetica", 12)
        text_description = """Text areas are assessed by two metrics: 1)text coverage, 2) non-text and text ratio(NTTR).
        The text coverage is for showing how the text layout in the whole image, and NTTR is for showing how the text layout relative to other non-text areas.
        A study shows that the text on the left side of visualisation could improve the user's comprehension compared to vertical layout which the text is above the visualisation[5]. According to the text and visualisation position distance, it is suggested that the text(e.g.: legend) should be placed near to the corresponding graphs to reduce eye movements[6]. The text in the visualisation should be not too much, but the adding back some useful text like text annotation would help with the interpretation of the visualisation[6]. Also, bigger and central text blocks would be assigned high saliency values[7], which means bigger and more central text blocks would gain more attention from people in the data visualisation. So unimportant text needs to have small areas.
        You could check the nttr distribution map. If the text coverage value is too low or nttr value is too high, you may need to increase the text areas.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(text_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
        self.pdf.drawText(textobject)
        image_filename =self.filename + '/submission_' + str(self.id)+ '/out1R.png'
        self.pdf.drawImage(image_filename, x=30, y=180, width=250, height=150)
        nttr__similarity_image_filename ='submissions/correlations/nttr_similarity.png'
        self.pdf.drawImage(nttr__similarity_image_filename, x=300, y=180, width=250, height=150)
        text_coverage__similarity_image_filename ='submissions/correlations/text_coverage_similarity.png'
        self.pdf.drawImage(text_coverage__similarity_image_filename, x=560, y=180, width=250, height=150)
        text_area_image_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/nttr_dist.png'
        self.pdf.drawImage(text_area_image_filename, x=30, y=20, width=250, height=150)
        nttr_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/nttr_result.png'
        self.pdf.drawImage(nttr_filename, x=300, y=30, width=250, height=150)
        text_coverage_result_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/text_coverage_result.png'
        self.pdf.drawImage(text_coverage_result_filename, x=560, y=30, width=250, height=150)

        
        
        
    def colour_page(self):
        # set the font and font size for the text
        self.pdf.setFont("Helvetica-Bold", 24)

        # draw the text in the center of the page
        text = "Colour Vision"
        self.pdf.drawCentredString(A4[1] / 2, A4[0] / 1.2, text)
        # set the font and font size for the unbold text
        start_point = self.start_point - self.line_distance
        availWidth, availHeight = 250*mm, A4[1]

        style = ParagraphStyle("justifies", alignment=TA_JUSTIFY, fontSize=11, leading=12)
        self.pdf.setFont("Helvetica", 12)
        colour_description = """There are two metrics to assess the colour vision of one submission: Colourfulnee and Weighted Affective Valence Estimates (WAVE)
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(colour_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        colourfulness_description = """Colourfulness is to show how colourful an image is, and the algorithms use standard deviations to calculate the values[3]. The higher, the more colourful this image is. 5 Dominant colours of your submission are extracted, it could help you understand the colourfulness of your submission together with the quantity value.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(colourfulness_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        WAVE_description = """This metric is to assess the colour preferences according to human aesthetic preferences towards certain colour[4]. The colour preference result is presented as a reference to check if your use of colour. 
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(WAVE_description, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        image_filename =self.filename + '/submission_' + str(self.id)+ '/out1R.png'
        self.pdf.drawImage(image_filename, x=30, y=200, width=250, height=150)
        colour_image_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/dominant_color.png'
        self.pdf.drawImage(colour_image_filename, x=300, y=200, width=250, height=150)
        wave_image_filename ='submissions/wave_preference.png'
        self.pdf.drawImage(wave_image_filename, x=560, y=200, width=250, height=150)
        wave_correlation_filename ='submissions/correlations/wave_similarity.png'
        self.pdf.drawImage(wave_correlation_filename, x=10, y=50, width=250, height=150)
        colourfulness_result_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/colourfulness_result.png'
        self.pdf.drawImage(colourfulness_result_filename, x=300, y=50, width=250, height=150)
        wave_result_filename =self.filename + '/submission_' + str(self.id)+ '/RESULTS/wave_result.png'
        self.pdf.drawImage(wave_result_filename, x=560, y=50, width=250, height=150)
        
        
    def reference_page(self):
        # set the font and font size for the text
        self.pdf.setFont("Helvetica-Bold", 24)

        # draw the text in the center of the page
        text = "References"
        self.pdf.drawCentredString(A4[1] / 2, A4[0] / 1.2, text)
        # set the font and font size for the unbold text
        start_point = self.start_point - self.line_distance
        availWidth, availHeight = 250*mm, A4[1]

        style = ParagraphStyle("justifies", alignment=TA_JUSTIFY, fontSize=11, leading=12)
        self.pdf.setFont("Helvetica", 12)
        self.pdf.drawString(A4[1] / 20, start_point, 'the style and layout design of this report is coming from:')
        start_point = start_point - self.line_distance
        style_reference = """[1]Nicolas Steven Holliman. Automating visualization quality assessment: a case study in
higher education. arXiv preprint arXiv:2106.00077, 2021.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        self.pdf.drawString(A4[1] / 20, start_point,'Saliency:')
        start_point = start_point - self.line_distance
        style_reference = """[1]https://pyimagesearch.com/2018/07/16/opencv-saliency-detection/
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        self.pdf.drawString(A4[1] / 20, start_point,'White Space:')
        start_point = start_point - self.line_distance
        style_reference = """[2]Aliaksei Miniukovich and Antonella De Angeli. Computation of interface aesthetics. In
Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Sys-
tems, pages 1163–1172,2015.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        self.pdf.drawString(A4[1] / 20, start_point,'Colourfulness:')
        start_point = start_point - self.line_distance
        style_reference = """[3]David Hasler and Sabine E Suesstrunk. Measuring colorfulness in natural images. In
Human vision and electronic imaging VIII, volume 5007, pages 87–95. SPIE, 2003.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        self.pdf.drawString(A4[1] / 20, start_point,'Colour Preference:')
        start_point = start_point - self.line_distance
        style_reference = """[4]Stephen E Palmer and Karen B Schloss. An ecological valence theory of human color
preference. Proceedings of the National Academy of Sciences, 107(19):8877–8882, 2010.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)
        
        self.pdf.drawString(A4[1] / 20, start_point,'Text Layout:')
        start_point = start_point - self.line_distance
        style_reference = """[5]Qiyu Zhi, Alvitta Ottley, and Ronald Metoyer. Linking and layout: Exploring the integration of text and visualization in storytelling. In Computer Graphics Forum, volume 38,
pages 675–685. Wiley Online Library, 2019.
[6]Stephanie Evergreen and Chris Metzner. Design principles for data visualization in evaluation. New Directions for Evaluation, 2013(140):5–20, 2013.
[7]Zoya Bylinskii, Nam Wook Kim, Peter O’Donovan, Sami Alsheikh, Spandan Madan,
Hanspeter Pfister, Fredo Durand, Bryan Russell, and Aaron Hertzmann. Learning visual importance for graphic designs and data visualizations. In Proceedings of the 30th
Annual ACM symposium on user interface software and technology, pages 57–69, 2017.
        """
        textobject = self.pdf.beginText(A4[1] / 20, start_point)
        lines = simpleSplit(style_reference, style.fontName, style.fontSize, availWidth)
        for line in lines:
            textobject.textLine(line.rstrip())
            start_point = start_point - self.line_distance
        self.pdf.drawText(textobject)

        