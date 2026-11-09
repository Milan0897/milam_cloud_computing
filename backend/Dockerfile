FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache openssl libc6-compat

COPY package*.json ./
RUN npm install && npm cache clean --force

COPY prisma ./prisma/
RUN npx prisma generate

COPY src ./src/

EXPOSE 5000

CMD ["npm", "run", "start:prod"]