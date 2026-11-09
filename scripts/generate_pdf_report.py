import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page numbers (Page X of Y)
    and include a running header and footer on every page except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber == 1:
            # Skip cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Running Header
        self.drawString(54, 755, "STUDENT DOCUMENT MANAGEMENT SYSTEM | ACADEMIC PROJECT REPORT")
        self.drawRightString(612 - 54, 755, "AWS CLOUD INFRASTRUCTURE")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 747, 612 - 54, 747)
        
        # Running Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Confidential - Submitted for Academic Evaluation | Milan Mandal")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#1A365D")    # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0")  # Royal Slate
    c_accent = colors.HexColor("#319795")     # Teal
    c_dark = colors.HexColor("#2D3748")       # Charcoal Body
    c_light = colors.HexColor("#F7FAFC")      # Light Gray Box
    c_border = colors.HexColor("#E2E8F0")     # Light Border
    c_card = colors.HexColor("#EDF2F7")       # Card Background

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=30
    )

    meta_label = ParagraphStyle(
        'CoverMetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_primary
    )

    meta_val = ParagraphStyle(
        'CoverMetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_dark
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=15,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2C5282")
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#234E52")
    )

    elements = []

    # ==========================================
    # COVER PAGE
    # ==========================================
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("ACADEMIC MAJOR PROJECT REPORT", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=12, textColor=c_accent, alignment=1, spaceAfter=15)))
    elements.append(Paragraph("STUDENT DOCUMENT MANAGEMENT SYSTEM", title_style))
    elements.append(Paragraph("A Cloud-Native, High-Security Academic Asset Vault on AWS (EC2 & S3)", subtitle_style))
    elements.append(HRFlowable(width="80%", thickness=2, color=c_secondary, spaceBefore=10, spaceAfter=30))

    cover_meta = [
        [Paragraph("Project Title:", meta_label), Paragraph("Student Document Management System (StudentDocs)", meta_val)],
        [Paragraph("Developer / Student:", meta_label), Paragraph("Milan Mandal", meta_val)],
        [Paragraph("Academic Stream:", meta_label), Paragraph("Computer Science & Engineering / Information Technology", meta_val)],
        [Paragraph("Hosting & Cloud:", meta_label), Paragraph("Amazon Web Services (AWS EC2 + AWS S3)", meta_val)],
        [Paragraph("Architecture Pattern:", meta_label), Paragraph("Containerized Multi-Tier Microservices (Docker & Nginx)", meta_val)],
        [Paragraph("Core Technologies:", meta_label), Paragraph("React 18, Node.js 20, Express, PostgreSQL 15, Prisma ORM", meta_val)],
        [Paragraph("Storage Security:", meta_label), Paragraph("Private S3 Bucket with Short-Lived Presigned URLs", meta_val)],
        [Paragraph("Project Status:", meta_label), Paragraph("Live & Fully Functional in Production (AWS Cloud)", meta_val)],
        [Paragraph("Deployment Region:", meta_label), Paragraph("AWS Asia Pacific (Sydney) [ap-southeast-2]", meta_val)],
        [Paragraph("Submission Year:", meta_label), Paragraph("2026", meta_val)],
    ]

    t_cover = Table(cover_meta, colWidths=[150, 320])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_cover)
    elements.append(Spacer(1, 40))

    callout_box = [
        [Paragraph("<b>Abstract:</b> This project demonstrates an end-to-end production web application that addresses the real-world challenge of student academic certificate and document loss. Leveraging AWS EC2 compute, private S3 object storage, PostgreSQL, and modern React 18, it guarantees multi-tenant data isolation, cryptographic security, fast uploads, instant previews, and seamless downloads.", callout_style)]
    ]
    t_callout = Table(callout_box, colWidths=[470])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E6FFFA")),
        ('BOX', (0, 0), (-1, -1), 1, c_accent),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(t_callout)

    elements.append(PageBreak())

    # ==========================================
    # SECTION 1: EXECUTIVE OVERVIEW & PROBLEM STATEMENT
    # ==========================================
    elements.append(Paragraph("1. Executive Overview & Problem Statement", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "Throughout academic life, students accumulate numerous critical physical and digital credentials, including semester marksheets, admit cards, university registration certificates, identity proofs, and character certificates. In traditional setups, students rely on unstructured email attachments, local mobile phone storage, or ad-hoc cloud drives. This leads to document fragmentation, file compression degradation, and frequent loss during emergency verification procedures.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Project Mission:</b> The <i>Student Document Management System</i> was designed, architected, and deployed to solve this problem by providing a centralized, secure, cloud-native document vault. Students can authenticate securely, categorize files by academic type, preview high-resolution PDFs and images inline, download credentials at full fidelity, and maintain private, tamper-proof document records accessible 24/7.",
        body_style
    ))

    # Key Objectives Bullet Points
    elements.append(Paragraph("<b>Primary Engineering Objectives:</b>", h2_style))
    elements.append(Paragraph("• <b>User-Level Data Isolation:</b> Absolute tenant segregation where no student can query, view, or manipulate another student's files (preventing IDOR vulnerabilities).", bullet_style))
    elements.append(Paragraph("• <b>Zero-Trust Cloud Storage:</b> Private AWS S3 bucket architecture where files are never made public. Access is governed exclusively via short-lived AWS presigned URLs.", bullet_style))
    elements.append(Paragraph("• <b>High Performance & Portability:</b> Containerized microservices using Docker Compose and Nginx reverse proxy, deployable on resource-constrained AWS EC2 Free-Tier instances.", bullet_style))
    elements.append(Paragraph("• <b>Seamless User Experience:</b> Responsive single-page application (SPA) with drag-and-drop file ingestion, client-side validation, live storage statistics, and instantaneous file downloads.", bullet_style))

    # ==========================================
    # SECTION 2: SYSTEM ARCHITECTURE & COMPONENT TOPOLOGY
    # ==========================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("2. System Architecture & Topology", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "The application utilizes a containerized 3-tier microservices architecture hosted on an AWS EC2 instance running Ubuntu Linux, integrated directly with Amazon Simple Storage Service (S3) for durable blob storage.",
        body_style
    ))

    arch_table_data = [
        [Paragraph("Layer", table_header), Paragraph("Component", table_header), Paragraph("Host / Port", table_header), Paragraph("Key Functional Responsibility", table_header)],
        [Paragraph("Client Layer", table_cell_bold), Paragraph("Web Browser", table_cell), Paragraph("Client Device", table_cell), Paragraph("Renders React SPA, handles client validations, sends authenticated REST requests.", table_cell)],
        [Paragraph("Web Proxy", table_cell_bold), Paragraph("Nginx (Alpine)", table_cell), Paragraph("EC2 : Port 80 (Public)", table_cell), Paragraph("Serves static Vite build, routes /api requests to backend, enforces 15MB upload limits.", table_cell)],
        [Paragraph("Application Tier", table_cell_bold), Paragraph("Express.js API", table_cell), Paragraph("EC2 : Port 5000 (Internal)", table_cell), Paragraph("JWT authentication, Multer file buffer intake, S3 presigned URL generation, CRUD logic.", table_cell)],
        [Paragraph("Metadata Store", table_cell_bold), Paragraph("PostgreSQL 15", table_cell), Paragraph("EC2 : Port 5432 (Internal)", table_cell), Paragraph("Stores user credentials, document metadata, S3 keys, and category tags via Prisma ORM.", table_cell)],
        [Paragraph("Object Storage", table_cell_bold), Paragraph("Amazon S3", table_cell), Paragraph("AWS S3 Cloud", table_cell), Paragraph("Durable private object storage, partition paths: users/{userId}/{category}/{uuid}.ext.", table_cell)],
    ]
    t_arch = Table(arch_table_data, colWidths=[80, 85, 105, 200])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t_arch)

    elements.append(PageBreak())

    # ==========================================
    # SECTION 3: TECHNOLOGY STACK & LANGUAGE MAPPING
    # ==========================================
    elements.append(Paragraph("3. Technology Stack & Language Breakdown", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "Each technology and programming language in the stack was deliberately chosen to ensure developer ergonomics, type safety, low memory footprint, and fast execution on AWS EC2.",
        body_style
    ))

    tech_data = [
        [Paragraph("Category", table_header), Paragraph("Technology / Library", table_header), Paragraph("Language / Runtime", table_header), Paragraph("Where Used & Purpose in Codebase", table_header)],
        [Paragraph("Frontend UI", table_cell_bold), Paragraph("React 18 + Vite 5", table_cell), Paragraph("JavaScript (ES6+)", table_cell), Paragraph("frontend/src/ - Component hierarchy, single page routing, responsive state.", table_cell)],
        [Paragraph("HTTP Client", table_cell_bold), Paragraph("Axios", table_cell), Paragraph("JavaScript", table_cell), Paragraph("frontend/src/api/ - Auto-attaches Bearer tokens and manages 401 logouts.", table_cell)],
        [Paragraph("Styling System", table_cell_bold), Paragraph("Custom CSS Variables", table_cell), Paragraph("CSS3", table_cell), Paragraph("frontend/src/styles.css - Responsive grid, modal dialogs, cards, toast popups.", table_cell)],
        [Paragraph("Backend Server", table_cell_bold), Paragraph("Express.js (Node 20)", table_cell), Paragraph("JavaScript (Node.js)", table_cell), Paragraph("backend/src/index.js - RESTful API controllers, routing, middleware pipeline.", table_cell)],
        [Paragraph("Data Access ORM", table_cell_bold), Paragraph("Prisma ORM 5.6", table_cell), Paragraph("Prisma Schema / JS", table_cell), Paragraph("backend/prisma/ - Automated schema migrations, connection pooling, queries.", table_cell)],
        [Paragraph("Database", table_cell_bold), Paragraph("PostgreSQL 15", table_cell), Paragraph("SQL / RDBMS", table_cell), Paragraph("Docker container postgres:15-alpine - Relational persistent metadata storage.", table_cell)],
        [Paragraph("Authentication", table_cell_bold), Paragraph("JWT + BCrypt.js", table_cell), Paragraph("JavaScript", table_cell), Paragraph("backend/src/controllers/authController.js - Password hashing (12 rounds) & JWT tokens.", table_cell)],
        [Paragraph("File Ingestion", table_cell_bold), Paragraph("Multer", table_cell), Paragraph("Node.js Middleware", table_cell), Paragraph("backend/src/routes/documentRoutes.js - In-memory streaming up to 10MB.", table_cell)],
        [Paragraph("Cloud SDK", table_cell_bold), Paragraph("AWS SDK v3", table_cell), Paragraph("Node.js SDK", table_cell), Paragraph("backend/src/services/s3Service.js - S3 PutObject, GetObject presigned URLs.", table_cell)],
        [Paragraph("Containerization", table_cell_bold), Paragraph("Docker & Compose", table_cell), Paragraph("Dockerfiles / YAML", table_cell), Paragraph("docker-compose.yml - Multi-container isolation, health checks, bridge networking.", table_cell)],
        [Paragraph("Cloud Server", table_cell_bold), Paragraph("Ubuntu 24.04 LTS", table_cell), Paragraph("Bash Shell", table_cell), Paragraph("deploy-ec2.sh - Automated OS tuning, swap memory generation, live updates.", table_cell)],
    ]
    t_tech = Table(tech_data, colWidths=[75, 95, 95, 205])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_tech)

    # ==========================================
    # SECTION 4: DATABASE DESIGN & SCHEMA ARCHITECTURE
    # ==========================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("4. Database Design & Schema Architecture", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "The relational database schema is managed through <b>Prisma ORM</b>, interfacing with <b>PostgreSQL 15</b>. Two core entities define the data model: <code>User</code> and <code>Document</code>, joined via a 1-to-many relationship with cascading delete rules.",
        body_style
    ))

    schema_data = [
        [Paragraph("Model", table_header), Paragraph("Field Name", table_header), Paragraph("Data Type", table_header), Paragraph("Constraints & Attributes", table_header), Paragraph("Description", table_header)],
        [Paragraph("User", table_cell_bold), Paragraph("id", table_cell), Paragraph("String", table_cell), Paragraph("@id @default(uuid())", table_cell), Paragraph("Primary Key (UUID v4)", table_cell)],
        [Paragraph("User", table_cell_bold), Paragraph("name", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL, length: 2-100", table_cell), Paragraph("Student Full Name", table_cell)],
        [Paragraph("User", table_cell_bold), Paragraph("email", table_cell), Paragraph("String", table_cell), Paragraph("@unique", table_cell), Paragraph("Student Email (Unique Index)", table_cell)],
        [Paragraph("User", table_cell_bold), Paragraph("password", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Bcrypt Hashed Password (cost 12)", table_cell)],
        [Paragraph("User", table_cell_bold), Paragraph("createdAt", table_cell), Paragraph("DateTime", table_cell), Paragraph("@default(now())", table_cell), Paragraph("Account Registration Timestamp", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("id", table_cell), Paragraph("String", table_cell), Paragraph("@id @default(uuid())", table_cell), Paragraph("Primary Key (UUID v4)", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("userId", table_cell), Paragraph("String", table_cell), Paragraph("Foreign Key, @@index", table_cell), Paragraph("References User(id) with Cascade", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("fileName", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("UUID-based S3 internal name", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("originalName", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Original upload filename (e.g. marksheet.pdf)", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("mimeType", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("application/pdf, image/jpeg, etc.", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("size", table_cell), Paragraph("Int", table_cell), Paragraph("NOT NULL (Bytes)", table_cell), Paragraph("Document file byte size", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("s3Key", table_cell), Paragraph("String", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Exact key path inside AWS S3 bucket", table_cell)],
        [Paragraph("Document", table_cell_bold), Paragraph("category", table_cell), Paragraph("String", table_cell), Paragraph("@default('other')", table_cell), Paragraph("marksheet, admin_card, id_proof, etc.", table_cell)],
    ]
    t_schema = Table(schema_data, colWidths=[65, 80, 65, 120, 140])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_schema)

    elements.append(PageBreak())

    # ==========================================
    # SECTION 5: STEP-BY-STEP APPLICATION WORKFLOWS
    # ==========================================
    elements.append(Paragraph("5. Step-by-Step Functional Workflows", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph("A. User Registration & Authentication Workflow", h2_style))
    elements.append(Paragraph(
        "1. <b>Client Ingestion:</b> Student inputs full name, email, password, and confirmation in <code>Register.jsx</code>.<br/>"
        "2. <b>Input Sanitization:</b> <code>express-validator</code> verifies valid email syntax, minimum password length (6 characters), and non-empty name.<br/>"
        "3. <b>Password Hashing:</b> Passwords are salted and hashed using <code>bcryptjs</code> with 12 computation rounds.<br/>"
        "4. <b>JWT Issuance:</b> Server generates a cryptographic JSON Web Token signed with a 64-character secret with a 7-day expiration.<br/>"
        "5. <b>Session Persistence:</b> Frontend stores the token in <code>localStorage</code>; Axios interceptor injects <code>Authorization: Bearer &lt;token&gt;</code> on all subsequent requests.",
        body_style
    ))

    elements.append(Paragraph("B. Document Upload & Cloud Storage Workflow", h2_style))
    elements.append(Paragraph(
        "1. <b>File Selection:</b> Student selects or drags a document into <code>Upload.jsx</code> (supports PDF, PNG, JPG, WebP up to 10MB).<br/>"
        "2. <b>Client Verification:</b> File MIME type and size are validated instantly before transmission; local preview is generated using <code>URL.createObjectURL</code>.<br/>"
        "3. <b>Multipart Streaming:</b> Frontend sends <code>multipart/form-data</code> to <code>POST /api/documents</code>.<br/>"
        "4. <b>S3 Partitioning:</b> Backend generates a collision-free UUID key and pushes the file buffer directly to S3 under <code>users/{userId}/{category}/{uuid}.ext</code>.<br/>"
        "5. <b>Metadata Commitment:</b> PostgreSQL record is saved with original filename, byte size, MIME type, S3 key, and category.",
        body_style
    ))

    elements.append(Paragraph("C. Document Preview & Instant Download Workflow", h2_style))
    elements.append(Paragraph(
        "1. <b>Presigned Security:</b> When <code>Dashboard.jsx</code> loads, backend uses AWS SDK's <code>getSignedUrl</code> to create time-limited presigned URLs (1-hour validity).<br/>"
        "2. <b>Inline Viewing:</b> Clicking <b>View</b> opens the presigned URL in a secure sandbox tab, allowing students to read documents or inspect marksheets in full quality.<br/>"
        "3. <b>Seamless Download:</b> Clicking the new <b>Download</b> button triggers an asynchronous blob retrieval with CORS headers, automatically downloading the file directly to the student's local machine retaining its exact <code>originalName</code> (e.g., <i>'10th_marksheet.pdf'</i>).<br/>"
        "4. <b>Live User Feedback:</b> Toast notifications inform the student: <i>'Starting download...'</i> followed by <i>'Downloaded successfully!'</i> upon completion.",
        body_style
    ))

    elements.append(Paragraph("D. Document Deletion Workflow", h2_style))
    elements.append(Paragraph(
        "1. <b>Confirmation Modal:</b> Clicking <b>Delete</b> opens a confirmation modal dialog to avoid accidental data loss.<br/>"
        "2. <b>Atomic Clean-Up:</b> Backend invokes AWS SDK <code>DeleteObjectCommand</code> to purge the physical file from S3, then executes <code>prisma.document.delete()</code> to remove the database entry.",
        body_style
    ))

    # ==========================================
    # SECTION 6: AWS CLOUD INFRASTRUCTURE & SECURITY
    # ==========================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("6. AWS Cloud Infrastructure & Security Architecture", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    aws_data = [
        [Paragraph("AWS Component", table_header), Paragraph("Resource Identifier", table_header), Paragraph("Configuration & Hardening Applied", table_header)],
        [Paragraph("EC2 Compute", table_cell_bold), Paragraph("milan-web-instance", table_cell), Paragraph("Ubuntu 24.04 LTS, 1GB Swap memory enabled, Docker runtime, public IP 15.134.209.196.", table_cell)],
        [Paragraph("Security Group", table_cell_bold), Paragraph("launch-wizard-sg", table_cell), Paragraph("Inbound: Port 22 (SSH admin), Port 80 (HTTP Web). Internal ports 5000 & 5432 completely closed.", table_cell)],
        [Paragraph("S3 Object Bucket", table_cell_bold), Paragraph("milan-web-s3-bucket", table_cell), Paragraph("Region ap-southeast-2 (Sydney). 'Block all public access' ENABLED. Custom CORS policy active.", table_cell)],
        [Paragraph("IAM Security User", table_cell_bold), Paragraph("milan-web-IAM", table_cell), Paragraph("Principle of Least Privilege: Restricted strictly to milan-web-s3-bucket. No access to other buckets.", table_cell)],
        [Paragraph("Docker Isolation", table_cell_bold), Paragraph("docker-compose.yml", table_cell), Paragraph("PostgreSQL & Express bind exclusively to 127.0.0.1 bridge network. Nginx is the sole gateway.", table_cell)],
    ]
    t_aws = Table(aws_data, colWidths=[95, 125, 250])
    t_aws.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t_aws)

    elements.append(PageBreak())

    # ==========================================
    # SECTION 7: SECURITY MATRIX & VULNERABILITY MITIGATION
    # ==========================================
    elements.append(Paragraph("7. Security Matrix & Vulnerability Defense", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "A rigorous defense-in-depth model ensures compliance with web security standards:",
        body_style
    ))

    sec_data = [
        [Paragraph("Threat / Vulnerability", table_header), Paragraph("Risk Level", table_header), Paragraph("Mitigation Mechanism in StudentDocs", table_header)],
        [Paragraph("Insecure Direct Object Reference (IDOR)", table_cell_bold), Paragraph("CRITICAL", table_cell_bold), Paragraph("Every database lookup for viewing or deleting verifies `userId: req.user.id`. Students cannot manipulate IDs.", table_cell)],
        [Paragraph("Public S3 Data Exposure", table_cell_bold), Paragraph("HIGH", table_cell_bold), Paragraph("Bucket public access is blocked. Files can only be accessed via signed URLs that automatically expire in 3600 seconds.", table_cell)],
        [Paragraph("SQL Injection Attacks", table_cell_bold), Paragraph("HIGH", table_cell_bold), Paragraph("Prisma ORM utilizes strongly-typed parameterized SQL queries, completely mitigating raw SQL injections.", table_cell)],
        [Paragraph("Credential Compromise", table_cell_bold), Paragraph("HIGH", table_cell_bold), Paragraph("Passwords salted with bcrypt (cost 12); plain text is never stored or logged in database or network.", table_cell)],
        [Paragraph("Out-Of-Memory DOS on EC2", table_cell_bold), Paragraph("MEDIUM", table_cell_bold), Paragraph("Automated 1GB swap memory allocation and Nginx body buffering prevent instance crashes on small VMs.", table_cell)],
        [Paragraph("Arbitrary File Upload Attack", table_cell_bold), Paragraph("HIGH", table_cell_bold), Paragraph("Strict MIME validation (PDF, JPG, PNG, WebP) on frontend and backend, with enforced 10MB size ceiling.", table_cell)],
    ]
    t_sec = Table(sec_data, colWidths=[120, 65, 285])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor("#C53030")), # Red Critical
        ('TEXTCOLOR', (1, 2), (1, 4), colors.HexColor("#DD6B20")), # Orange High
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_sec)

    # ==========================================
    # SECTION 8: VERIFICATION RESULTS & SYSTEM METRICS
    # ==========================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("8. Live System Verification & Deployment Results", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    results_data = [
        [Paragraph("Feature / Module", table_header), Paragraph("Test Case Description", table_header), Paragraph("Observed Result", table_header), Paragraph("Status", table_header)],
        [Paragraph("User Signup & Login", table_cell_bold), Paragraph("New user registration with email and password hashing.", table_cell), Paragraph("Account created, JWT stored, redirected to Dashboard.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("Document Upload", table_cell_bold), Paragraph("Uploading 5MB academic marksheet PDF with category tag.", table_cell), Paragraph("Stored to S3 ap-southeast-2, record added to PostgreSQL.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("Inline Preview", table_cell_bold), Paragraph("Clicking 'View' on PDF and image cards.", table_cell), Paragraph("Presigned URL generated; displays in browser tab.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("Document Download", table_cell_bold), Paragraph("Clicking 'Download' button on document card.", table_cell), Paragraph("File saved locally preserving original academic filename.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("Category Filtering", table_cell_bold), Paragraph("Filtering cards by Marksheet, Admit Card, ID Proof.", table_cell), Paragraph("Grid instantly updates showing relevant category assets.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("Document Deletion", table_cell_bold), Paragraph("Confirming document deletion from modal.", table_cell), Paragraph("Object deleted from S3 and record purged from database.", table_cell), Paragraph("PASS", table_cell_bold)],
        [Paragraph("EC2 Health & Stability", table_cell_bold), Paragraph("24-hour continuous uptime test on t2.micro.", table_cell), Paragraph("Zero downtime, swap memory ensures zero OOM crashes.", table_cell), Paragraph("PASS", table_cell_bold)],
    ]
    t_res = Table(results_data, colWidths=[95, 140, 185, 50])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor("#22543D")), # Green Pass
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_res)

    # ==========================================
    # SECTION 9: CONCLUSION & FUTURE ENHANCEMENTS
    # ==========================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("9. Conclusion & Future Roadmap", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "The <b>Student Document Management System</b> has been successfully conceptualized, built, tested, and deployed to production on AWS. It demonstrates the seamless union of modern client-side engineering (React 18), robust API microservices (Express & Prisma), reliable database persistence (PostgreSQL), and enterprise cloud storage (AWS S3 & EC2). The system fulfills all academic requirements while meeting industry standards of security, scalability, and performance.",
        body_style
    ))
    elements.append(Paragraph("<b>Planned Future Roadmap:</b>", h2_style))
    elements.append(Paragraph("• <b>OCR Marksheet Extraction:</b> Integrating AWS Textract to automatically scan grades and GPA from uploaded marksheets into student records.", bullet_style))
    elements.append(Paragraph("• <b>Custom Domain & SSL/TLS:</b> Binding a custom institution domain (e.g., docs.college.edu) with automated Let's Encrypt SSL certificates.", bullet_style))
    elements.append(Paragraph("• <b>Time-Limited Public Sharing:</b> Enabling students to generate secure, password-protected temporary links to share specific documents with recruiters.", bullet_style))
    elements.append(Paragraph("• <b>Two-Factor Authentication (2FA):</b> Adding TOTP or email OTP verification during login for enhanced identity protection.", bullet_style))

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=5, spaceAfter=15))

    # Signature Block
    sig_data = [
        [Paragraph("<b>Student Signature:</b>", meta_label), Paragraph("<b>Faculty / Examiner Signature:</b>", meta_label)],
        [Spacer(1, 25), Spacer(1, 25)],
        [Paragraph("____________________________<br/>Milan Mandal<br/>Date: ____________________", body_style),
         Paragraph("____________________________<br/>Department of Computer Science<br/>Date: ____________________", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[235, 235])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(t_sig)

    # Build Document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully at: {filename}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "Student_Document_Management_System_Project_Report.pdf"
    build_pdf(out_path)
