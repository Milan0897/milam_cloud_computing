import { PutObjectCommand, DeleteObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import s3Client from '../config/s3.js';
import { v4 as uuidv4 } from 'uuid';

const BUCKET_NAME = process.env.AWS_S3_BUCKET;

export const uploadToS3 = async (file, userId, category = 'other') => {
  const fileExtension = file.originalname.split('.').pop();
  const fileName = `${uuidv4()}.${fileExtension}`;
  const s3Key = `users/${userId}/${category}/${fileName}`;

  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
    Body: file.buffer,
    ContentType: file.mimetype,
  });

  await s3Client.send(command);

  return {
    s3Key,
    fileName,
    originalName: file.originalname,
    mimeType: file.mimetype,
    size: file.size,
  };
};

export const deleteFromS3 = async (s3Key) => {
  const command = new DeleteObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
  });

  await s3Client.send(command);
};

export const getPresignedUrl = async (s3Key, expiresIn = 3600) => {
  const command = new GetObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
  });

  return getSignedUrl(s3Client, command, { expiresIn });
};

export const getPresignedUploadUrl = async (userId, fileName, fileType, category = 'other') => {
  const fileExtension = fileName.split('.').pop();
  const uniqueFileName = `${uuidv4()}.${fileExtension}`;
  const s3Key = `users/${userId}/${category}/${uniqueFileName}`;

  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
    ContentType: fileType,
  });

  const uploadUrl = await getSignedUrl(s3Client, command, { expiresIn: 3600 });

  return {
    uploadUrl,
    s3Key,
    fileName: uniqueFileName,
  };
};