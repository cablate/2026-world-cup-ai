FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules/serve ./node_modules/serve
EXPOSE 3000
CMD ["npx", "serve", "dist", "-l", "3000", "--no-clipboard"]
