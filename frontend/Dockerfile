FROM node:18-alpine

COPY package.json .
RUN npm install
COPY . .
ARG NEXT_PUBLIC_BASE_API_URL
ENV NEXT_PUBLIC_BASE_API_URL=${NEXT_PUBLIC_BASE_API_URL}
RUN npm run build
CMD npm run start
