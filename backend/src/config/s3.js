import { S3Client } from '@aws-sdk/client-s3';

const s3Config = {
  region: process.env.AWS_REGION || 'us-east-1',
};

// If explicit credentials are provided, use them.
// Otherwise, AWS SDK automatically falls back to EC2 IAM Role instance profile.
if (process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY) {
  s3Config.credentials = {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  };
}

const s3Client = new S3Client(s3Config);

export default s3Client;