FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
COPY ./src/assets .


RUN npm run build

CMD ["npm", "run", "dev", "--", "--host"]
