import prisma from '../config/database.js';
import {
  uploadToS3,
  deleteFromS3,
  getPresignedUrl,
  getPresignedUploadUrl,
} from '../services/s3Service.js';

const ALLOWED_TYPES = [
  'application/pdf',
  'image/jpeg',
  'image/png',
  'image/jpg',
  'image/webp',
];

const MAX_FILE_SIZE = 10 * 1024 * 1024;

export const uploadDocument = async (req, res) => {
  try {
    const file = req.file;
    const { category } = req.body;

    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    if (!ALLOWED_TYPES.includes(file.mimetype)) {
      return res.status(400).json({ error: 'Only PDF, JPEG, PNG, and WebP files allowed' });
    }

    if (file.size > MAX_FILE_SIZE) {
      return res.status(400).json({ error: 'File size must be less than 10MB' });
    }

    const uploadResult = await uploadToS3(file, req.user.id, category || 'other');

    const document = await prisma.document.create({
      data: {
        userId: req.user.id,
        fileName: uploadResult.fileName,
        originalName: uploadResult.originalName,
        mimeType: uploadResult.mimeType,
        size: uploadResult.size,
        s3Key: uploadResult.s3Key,
        category: category || 'other',
      },
    });

    res.status(201).json({ document });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Upload failed' });
  }
};

export const getDocuments = async (req, res) => {
  try {
    const { category } = req.query;

    const where = { userId: req.user.id };
    if (category && category !== 'all') {
      where.category = category;
    }

    const documents = await prisma.document.findMany({
      where,
      orderBy: { createdAt: 'desc' },
    });

    const documentsWithUrls = await Promise.all(
      documents.map(async (doc) => {
        const viewUrl = await getPresignedUrl(doc.s3Key);
        return { ...doc, viewUrl };
      })
    );

    res.json({ documents: documentsWithUrls });
  } catch (error) {
    console.error('Get documents error:', error);
    res.status(500).json({ error: 'Failed to fetch documents' });
  }
};

export const getDocument = async (req, res) => {
  try {
    const { id } = req.params;

    const document = await prisma.document.findFirst({
      where: { id, userId: req.user.id },
    });

    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }

    const viewUrl = await getPresignedUrl(document.s3Key);
    res.json({ document: { ...document, viewUrl } });
  } catch (error) {
    console.error('Get document error:', error);
    res.status(500).json({ error: 'Failed to fetch document' });
  }
};

export const deleteDocument = async (req, res) => {
  try {
    const { id } = req.params;

    const document = await prisma.document.findFirst({
      where: { id, userId: req.user.id },
    });

    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }

    await deleteFromS3(document.s3Key);
    await prisma.document.delete({ where: { id } });

    res.json({ message: 'Document deleted successfully' });
  } catch (error) {
    console.error('Delete document error:', error);
    res.status(500).json({ error: 'Failed to delete document' });
  }
};

export const getPresignedUpload = async (req, res) => {
  try {
    const { fileName, fileType, category } = req.body;

    if (!ALLOWED_TYPES.includes(fileType)) {
      return res.status(400).json({ error: 'Invalid file type' });
    }

    const result = await getPresignedUploadUrl(req.user.id, fileName, fileType, category);
    res.json(result);
  } catch (error) {
    console.error('Presigned upload error:', error);
    res.status(500).json({ error: 'Failed to generate upload URL' });
  }
};

export const getCategories = async (req, res) => {
  const categories = [
    { value: 'marksheet', label: 'Marksheet' },
    { value: 'admin_card', label: 'Admin Card' },
    { value: 'registration_certificate', label: 'Registration Certificate' },
    { value: 'id_proof', label: 'ID Proof' },
    { value: 'other', label: 'Other' },
  ];
  res.json({ categories });
};