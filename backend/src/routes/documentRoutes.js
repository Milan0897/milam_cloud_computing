import { Router } from 'express';
import multer from 'multer';
import {
  uploadDocument,
  getDocuments,
  getDocument,
  deleteDocument,
  getPresignedUpload,
  getCategories,
} from '../controllers/documentController.js';
import { authenticateToken } from '../middleware/auth.js';

const router = Router();

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg', 'image/webp'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Only PDF, JPEG, PNG, and WebP files allowed'), false);
    }
  },
});

router.use(authenticateToken);

router.get('/categories', getCategories);
router.get('/', getDocuments);
router.post('/presigned-upload', getPresignedUpload);
router.get('/:id', getDocument);
router.post('/', upload.single('file'), uploadDocument);
router.delete('/:id', deleteDocument);

export default router;