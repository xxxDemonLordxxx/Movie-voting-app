FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
COPY ./src/assets .

COPY ./public/navigationicons .


RUN npm run build

CMD ["npm", "run", "dev", "--", "--host"]
