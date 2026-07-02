"""
PDF Generator Utility for Question Papers
"""
import os
import base64
import uuid
import logging
from io import BytesIO
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

logger = logging.getLogger(__name__)

class QuestionPaperPDFGenerator:
    """Utility class to generate PDF from question paper data"""
    
    @staticmethod
    def generate_pdf(paper_data, logo_image=None, request=None):
        """
        Generate PDF from paper data
        
        Args:
            paper_data (dict): Contains all paper information
            logo_image (bytes/str, optional): Logo image data or path
            request (HttpRequest, optional): Request object for context
            
        Returns:
            bytes: PDF content as bytes
        """
        try:
            logger.info(f"Starting PDF generation for: {paper_data.get('exam_name', 'Unknown')}")
            
            # Create HTML content
            html_content = QuestionPaperPDFGenerator.create_html_content(paper_data, logo_image)
            
            if not html_content:
                logger.error("Failed to create HTML content")
                return None
            
            # Create PDF using xhtml2pdf
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(
                BytesIO(html_content.encode('utf-8')),
                dest=pdf_buffer,
                encoding='utf-8',
                link_callback=QuestionPaperPDFGenerator.link_callback
            )
            
            if pisa_status.err:
                logger.error(f"PDF generation error: {pisa_status.err}")
                return None
            
            # Get PDF bytes
            pdf_buffer.seek(0)
            pdf_bytes = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            logger.info(f"PDF generated successfully: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def create_html_content(paper_data, logo_image=None):
        """Create HTML content for the paper"""
        try:
            # Prepare context for template
            context = {
                'paper': paper_data,
                'logo_image': logo_image,
                'current_date': datetime.now().strftime('%d %B %Y'),
                'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            # Process logo
            if logo_image and isinstance(logo_image, bytes):
                # Convert bytes to base64 for embedding in HTML
                logo_base64 = base64.b64encode(logo_image).decode('utf-8')
                context['logo_base64'] = logo_base64
                context['logo_data_url'] = f"data:image/png;base64,{logo_base64}"
            elif logo_image and isinstance(logo_image, str) and os.path.exists(logo_image):
                # Read logo file
                with open(logo_image, 'rb') as f:
                    logo_bytes = f.read()
                    logo_base64 = base64.b64encode(logo_bytes).decode('utf-8')
                    context['logo_base64'] = logo_base64
                    context['logo_data_url'] = f"data:image/png;base64,{logo_base64}"
            
            # Process watermark
            if paper_data.get('watermark'):
                watermark = paper_data['watermark']
                context['watermark'] = {
                    'text': watermark.get('text', 'CONFIDENTIAL'),
                    'opacity': watermark.get('opacity', 0.1),
                    'size': watermark.get('size', '120px'),
                }
            
            # Process signatures
            if paper_data.get('signatures'):
                context['signatures'] = paper_data['signatures']
            
            # Process additional elements
            if paper_data.get('additional_elements'):
                context['additional_elements'] = paper_data['additional_elements']
            
            # Process sections
            sections = paper_data.get('sections', [])
            if not sections:
                # Create default sections from questions
                sections = QuestionPaperPDFGenerator.organize_questions_into_sections(
                    paper_data.get('questions', []),
                    paper_data.get('selected_questions', [])
                )
            context['sections'] = sections
            
            # Format exam date
            exam_date = paper_data.get('exam_date')
            if exam_date:
                try:
                    if isinstance(exam_date, str):
                        date_obj = datetime.strptime(exam_date, '%Y-%m-%d')
                        context['exam_date_formatted'] = date_obj.strftime('%d %B %Y')
                    else:
                        context['exam_date_formatted'] = exam_date.strftime('%d %B %Y')
                except:
                    context['exam_date_formatted'] = str(exam_date)
            else:
                context['exam_date_formatted'] = ''
            
            # Generate HTML using template
            html = render_to_string('pdf/question_paper_template.html', context)
            
            return html
            
        except Exception as e:
            logger.error(f"Error creating HTML content: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def organize_questions_into_sections(all_questions, selected_question_ids):
        """Organize questions into sections based on type"""
        sections = []
        
        # Get selected questions
        selected_questions = []
        for q_id in selected_question_ids:
            question = next((q for q in all_questions if str(q.get('id')) == str(q_id)), None)
            if question:
                selected_questions.append(question)
        
        if not selected_questions:
            return sections
        
        # Group questions by type
        questions_by_type = {}
        for question in selected_questions:
            q_type = question.get('type', 'descriptive')
            if q_type not in questions_by_type:
                questions_by_type[q_type] = []
            questions_by_type[q_type].append(question)
        
        # Create sections
        section_definitions = {
            'objective': {
                'title': 'Section A: Objective Questions',
                'instructions': 'Choose the correct option for each question.',
            },
            'mcq': {
                'title': 'Section A: Multiple Choice Questions',
                'instructions': 'Choose the correct option for each question.',
            },
            'descriptive': {
                'title': 'Section B: Descriptive Questions',
                'instructions': 'Answer the following questions in detail.',
            },
            'numerical': {
                'title': 'Section C: Numerical Problems',
                'instructions': 'Solve the following numerical problems. Show all steps.',
            },
            'short_answer': {
                'title': 'Section D: Short Answer Questions',
                'instructions': 'Answer the following questions briefly.',
            },
            'true_false': {
                'title': 'Section E: True or False',
                'instructions': 'State whether the following statements are True or False.',
            },
            'match_following': {
                'title': 'Section F: Match the Following',
                'instructions': 'Match the items in Column A with Column B.',
            },
            'fill_in_the_blanks': {
                'title': 'Section G: Fill in the Blanks',
                'instructions': 'Fill in the blanks with appropriate words.',
            },
        }
        
        section_order = ['objective', 'mcq', 'true_false', 'match_following', 'fill_in_the_blanks', 
                        'short_answer', 'numerical', 'descriptive']
        
        section_counter = 0
        for section_type in section_order:
            if section_type in questions_by_type and questions_by_type[section_type]:
                section_counter += 1
                section_letter = chr(64 + section_counter)  # A, B, C, etc.
                
                section_info = section_definitions.get(section_type, {
                    'title': f'Section {section_letter}: Questions',
                    'instructions': 'Answer the following questions.'
                })
                
                sections.append({
                    'title': section_info['title'],
                    'instructions': section_info['instructions'],
                    'questions': QuestionPaperPDFGenerator.format_questions_for_display(
                        questions_by_type[section_type]
                    )
                })
        
        return sections
    
    @staticmethod
    def format_questions_for_display(questions):
        """Format questions for HTML display"""
        formatted_questions = []
        
        for question in questions:
            formatted_q = {
                'id': question.get('id'),
                'question_text': question.get('question', ''),
                'marks': question.get('marks', 1),
                'type': question.get('type', 'descriptive'),
                'subject': question.get('subject_name', ''),
                'chapter': question.get('chapter', ''),
                'topic': question.get('topic', ''),
                'difficulty': question.get('difficulty', 'medium'),
            }
            
            # Add options for MCQ/Objective questions
            if formatted_q['type'] in ['objective', 'mcq']:
                options = []
                for i in range(1, 6):
                    option_text = question.get(f'option{i}')
                    if option_text:
                        options.append({
                            'letter': chr(64 + i),  # A, B, C, D, E
                            'text': option_text
                        })
                if options:
                    formatted_q['options'] = options
                    
                    # Add correct answer if available
                    correct_answer = question.get('correct_answer') or question.get('correct_options')
                    if correct_answer:
                        formatted_q['correct_answer'] = correct_answer
            
            # Add answer for other question types
            elif formatted_q['type'] in ['true_false', 'fill_in_the_blanks', 'short_answer']:
                answer = question.get('answer')
                if answer:
                    formatted_q['answer'] = answer
            
            formatted_questions.append(formatted_q)
        
        return formatted_questions
    
    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        try:
            # Handle data URIs
            if uri.startswith("data:"):
                return uri
            
            # Handle absolute URLs
            if uri.startswith('http://') or uri.startswith('https://'):
                return uri
            
            # Handle relative URLs
            if uri.startswith('/'):
                # For static files
                if uri.startswith('/static/'):
                    path = os.path.join(settings.STATIC_ROOT, uri[8:])
                # For media files
                elif uri.startswith('/media/'):
                    path = os.path.join(settings.MEDIA_ROOT, uri[7:])
                else:
                    path = os.path.join(settings.BASE_DIR, uri[1:])
            else:
                # Relative path
                path = os.path.join(settings.BASE_DIR, uri)
            
            # Make sure the file exists
            if os.path.isfile(path):
                return path
            else:
                logger.warning(f"File not found for PDF generation: {uri}")
                return None
                
        except Exception as e:
            logger.error(f"Error in link callback for URI {uri}: {str(e)}")
            return None
    
    @staticmethod
    def save_pdf_to_file(pdf_bytes, filename_prefix="question_paper"):
        """
        Save PDF bytes to a file in the media directory
        
        Args:
            pdf_bytes (bytes): PDF content
            filename_prefix (str): Prefix for the filename
            
        Returns:
            str: Relative file path (for storing in FileField)
        """
        try:
            # Create directory if it doesn't exist
            pdf_dir = os.path.join(settings.MEDIA_ROOT, 'question_papers', 'pdfs')
            os.makedirs(pdf_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = uuid.uuid4().hex[:8]
            safe_prefix = filename_prefix.replace(' ', '_').replace('/', '_')[:50]
            filename = f"{safe_prefix}_{timestamp}_{unique_id}.pdf"
            filepath = os.path.join(pdf_dir, filename)
            
            # Save PDF
            with open(filepath, 'wb') as f:
                f.write(pdf_bytes)
            
            # Return relative path for FileField
            relative_path = os.path.join('question_papers', 'pdfs', filename)
            logger.info(f"PDF saved to: {relative_path}")
            
            return relative_path
            
        except Exception as e:
            logger.error(f"Error saving PDF to file: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def save_logo_image(logo_data, filename_prefix="logo"):
        """
        Save logo image to a file
        
        Args:
            logo_data (bytes/UploadedFile): Logo image data
            filename_prefix (str): Prefix for the filename
            
        Returns:
            str: Relative file path
        """
        try:
            # Create directory if it doesn't exist
            logo_dir = os.path.join(settings.MEDIA_ROOT, 'question_papers', 'logos')
            os.makedirs(logo_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = uuid.uuid4().hex[:8]
            safe_prefix = filename_prefix.replace(' ', '_').replace('/', '_')[:50]
            filename = f"{safe_prefix}_{timestamp}_{unique_id}.png"
            filepath = os.path.join(logo_dir, filename)
            
            # Save logo
            if isinstance(logo_data, bytes):
                with open(filepath, 'wb') as f:
                    f.write(logo_data)
            else:
                # Assuming it's a Django UploadedFile
                with open(filepath, 'wb+') as f:
                    for chunk in logo_data.chunks():
                        f.write(chunk)
            
            # Return relative path
            relative_path = os.path.join('question_papers', 'logos', filename)
            logger.info(f"Logo saved to: {relative_path}")
            
            return relative_path
            
        except Exception as e:
            logger.error(f"Error saving logo image: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def create_pdf_from_scratch(paper_data):
        """
        Alternative method using ReportLab for more control over PDF generation
        """
        try:
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch, cm
            
            # Create buffer for PDF
            buffer = BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
            )
            
            # Create story (content)
            story = []
            styles = getSampleStyleSheet()
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                alignment=1,  # Center
                spaceAfter=30,
            )
            
            story.append(Paragraph(paper_data.get('exam_name', 'Question Paper'), title_style))
            story.append(Spacer(1, 12))
            
            # Add exam details
            details = [
                f"<b>Class:</b> {paper_data.get('class_name', '')}",
                f"<b>Course:</b> {paper_data.get('course_name', '')}",
                f"<b>Total Marks:</b> {paper_data.get('total_marks', 100)}",
                f"<b>Time Duration:</b> {paper_data.get('time_duration', '3 hours')}",
                f"<b>Date:</b> {paper_data.get('exam_date_formatted', '')}",
            ]
            
            for detail in details:
                story.append(Paragraph(detail, styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 24))
            
            # Add instructions
            if paper_data.get('instructions'):
                story.append(Paragraph("<b>General Instructions:</b>", styles['Heading2']))
                story.append(Spacer(1, 6))
                instructions = paper_data['instructions'].split('\n')
                for instruction in instructions:
                    if instruction.strip():
                        story.append(Paragraph(f"• {instruction.strip()}", styles['Normal']))
                        story.append(Spacer(1, 3))
                story.append(Spacer(1, 24))
            
            # Add questions
            question_number = 1
            sections = paper_data.get('sections', [])
            
            for section in sections:
                # Section title
                story.append(Paragraph(f"<b>{section.get('title', 'Questions')}</b>", styles['Heading2']))
                story.append(Spacer(1, 6))
                
                # Section instructions
                if section.get('instructions'):
                    story.append(Paragraph(f"<i>{section['instructions']}</i>", styles['Italic']))
                    story.append(Spacer(1, 12))
                
                # Questions in this section
                for question in section.get('questions', []):
                    # Question text
                    q_text = f"<b>{question_number}.</b> {question.get('question_text', '')}"
                    story.append(Paragraph(q_text, styles['Normal']))
                    story.append(Spacer(1, 6))
                    
                    # Options for MCQ
                    if question.get('options'):
                        for option in question['options']:
                            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;({option['letter']}) {option['text']}", styles['Normal']))
                            story.append(Spacer(1, 3))
                    
                    # Marks
                    story.append(Paragraph(f"<i>[{question.get('marks', 1)} Mark(s)]</i>", styles['Italic']))
                    story.append(Spacer(1, 12))
                    
                    question_number += 1
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error creating PDF with ReportLab: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def validate_paper_data(paper_data):
        """Validate paper data before generating PDF"""
        errors = []
        
        # Check required fields
        required_fields = ['exam_name', 'total_marks']
        for field in required_fields:
            if not paper_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Check questions
        if not paper_data.get('selected_questions') and not paper_data.get('questions'):
            errors.append("No questions selected for the paper")
        
        # Check total marks
        try:
            total_marks = int(paper_data.get('total_marks', 0))
            if total_marks <= 0:
                errors.append("Total marks must be greater than 0")
        except:
            errors.append("Invalid total marks value")
        
        return errors