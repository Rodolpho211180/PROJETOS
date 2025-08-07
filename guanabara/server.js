const express = require('express');
const bodyParser = require('body-parser');
const firebird = require('node-firebird');
const path = require('path');

const app = express();
const PORT = 3000;

const options = {
  host: 'localhost',
  port: 3050,
  database: 'C:\\RESWINCS\\Banco\\RESULTH.FB',
  user: 'SYSDBA',
  password: 'masterkey',
  lowercase_keys: false,
  role: null,
  pageSize: 4096
};

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Página inicial
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Rota do relatório
app.post('/index', (req, res) => {
  const {
    codprod,
    data_inicio,
    data_fim,
    dia_semana,
    mes,
    hora_inicio,
    hora_fim
  } = req.body;

  let query = `
    SELECT 
      p.datapedido,
      pr.descricao,
      SUM(i.quantidade) AS qtd_total_dia,
      SUM(i.quantidade * i.precounit) AS total_dia
    FROM 
      pedidoc p
    JOIN 
      pedidoi i ON p.codpedido = i.codpedido
    JOIN 
      produto pr ON i.codprod = pr.codprod
    WHERE 
      p.datapedido BETWEEN ? AND ?
      AND i.codprod = ?
  `;

  const params = [data_inicio, data_fim, codprod];

  if (dia_semana !== '') {
    query += ' AND EXTRACT(WEEKDAY FROM p.datapedido) = ?';
    params.push(parseInt(dia_semana));
  }

  if (mes !== '') {
    query += ' AND EXTRACT(MONTH FROM p.datapedido) = ?';
    params.push(parseInt(mes));
  }

  if (hora_inicio && hora_fim) {
    query += ' AND p.hora BETWEEN ? AND ?';
    params.push(hora_inicio, hora_fim);
  }

  query += `
    GROUP BY 
      p.datapedido, pr.descricao
    ORDER BY 
      p.datapedido
  `;

  firebird.attach(options, (err, db) => {
    if (err) return res.send("Erro ao conectar ao banco: " + err.message);

    db.query(query, params, (err, result) => {
      db.detach();

      if (err) return res.send("Erro na consulta: " + err.message);
      if (!result.length) return res.send("Nenhum dado encontrado para os filtros.");

      // HTML com referência ao CSS
      let html = `
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
          <meta charset="UTF-8">
          <title>Relatório de Vendas</title>
          <link rel="stylesheet" href="/style.css">
        </head>
        <body>
          <h1>Relatório de Vendas por Produto</h1>
          <p>Produto: <strong>${codprod}</strong></p>
          <p>Período: <strong>${data_inicio}</strong> a <strong>${data_fim}</strong></p>
      `;

      if (dia_semana !== '') {
        const dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
        html += `<p>Dia da Semana: <strong>${dias[parseInt(dia_semana)]}</strong></p>`;
      }

      if (mes !== '') {
        const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
        html += `<p>Mês: <strong>${meses[parseInt(mes) - 1]}</strong></p>`;
      }

      if (hora_inicio && hora_fim) {
        html += `<p>Horário: <strong>${hora_inicio}</strong> até <strong>${hora_fim}</strong></p>`;
      }

      html += `
        <table>
          <thead>
            <tr>
              <th>Data do Pedido</th>
              <th>Descrição</th>
              <th>Quantidade Total do Dia</th>
              <th>Total do Dia (R$)</th>
            </tr>
          </thead>
          <tbody>
      `;

      let totalGeral = 0;

      result.forEach(row => {
        html += `
          <tr>
            <td>${new Date(row.DATAPEDIDO).toLocaleString('pt-BR')}</td>
            <td>${row.DESCRICAO}</td>
            <td>${row.QTD_TOTAL_DIA}</td>
            <td>${row.TOTAL_DIA.toFixed(2)}</td>
          </tr>
        `;
        totalGeral += row.TOTAL_DIA;
      });

      html += `
          </tbody>
        </table>
        <h3>Total Geral: R$ ${totalGeral.toFixed(2)}</h3>
        <a href="/">Voltar</a>
        </body>
        </html>
      `;

      res.send(html);
    });
  });
});

app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
