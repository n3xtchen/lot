/*
 * app.js
 * Copyright (C) 2016 n3xtchen <echenwen@gmail.com>
 *
 * Distributed under terms of the GPL-2.0 license.
 */

var restify = require('restify');
var Node = require("./models").Node;
var Link = require("./models").Link;

// hello world
function respond(req, res, next) {
  res.send('hello ' + req.params.name);
  next();
}

// 服务器配置
var server = restify.createServer({
  name: 'traffic_wonder',
  version: '1.0.0'
});
server.use(restify.queryParser());
server.use(restify.bodyParser());

server.get('/hello/:name', respond);
server.head('/hello/:name', respond);

// 初始化数据
server.post('/db/init', function(req, res) {
  Node.sync({force: true});
  Link.sync({force: true});
  res.json({"message" : "数据库初始化成功!"});
})

// 数据库操作
// List
server.get('/nodes', function(req, res, next) {
  var qs = req.query;
  Node.findAll({
    offset: qs.offset||1,
    limit: qs.limit||10
  }).then(function(data) {
    var result = data.map(function(row) { 
      var res = JSON.parse(row.props);
      res.id = row.id;
      return res;
    });
    res.json({"data": result});
  });
});

// C
server.post('/node', function(req, res, next) {
  var data = JSON.parse(req.body);
  Node.findOrCreate({
      name: data.name,
      default
  }).spread(function(node, created) {
    res.json({"" : "节点创建成功(id:" + this.lastID + ")!"});
  }).catch(function(error) {
    res.json({"message" : error.message});
  });
})

// R
server.get('/node/:id', function(req, res, next) {
  Node.findById(req.params.id).then(function(node) {
    if (!node) throw new Error("not found");
    res.json({"data" : JSON.parse(node.get("props"))});
  }).catch(function(error) {
    res.json({"message" : error.message});
  });
})

// U
server.put('/node/:id', function(req, res, next) {
  db.run("UPDATE nodes SET props = ? WHERE id = ?", [
    req.body, req.params.id
  ], function(err){
    if (err) throw err;
    res.json({"data" : this.changes});
  });
})

// D
server.del('/node/:id', function(req, res, next) {
  db.run("DELETE FROM nodes WHERE id = ?", req.params.id, function(err){
    if (err) throw err;
    res.json({"data" : this.changes});
  });
})

// add link
server.post('/link/:source/:target', function(req, res, next) {
  var source = req.params.source;
  var target = req.params.target;
  db.run("INSERT INTO links (source, target, props) values (?, ?, ?)", [
    source, target, req.body
  ], function(err) {
    if (err) res.json(err);
    else res.json({"message" : "连接创建成功(id:" + this.lastID + ","
      + source + "->" + target + ")!"});
  });
})

// update link
server.put('/link/:source/:target', function(req, res, next) {
  var source = req.params.source;
  var target = req.params.target;
  db.run("update links set props = ? where source = ? and target = ?", [
    req.body, source, target
  ], function(err) {
    if (err) res.json(err);
    else res.json({"message" : "连接更新成功(id:" + this.lastID + ","
      + source + "->" + target + ")!", code: this.changes});
  });
})

// delete link
server.del('/link/:source/:target', function(req, res, next) {
  var source = req.params.source;
  var target = req.params.target;
  db.run("DELETE FROM links WHERE source = ? AND target = ?", [
    source, target
  ], function(err) {
    if (err) res.json(err);
    else res.json({"message" : "连接删除成功(id:" + this.lastID + ","
      + source + "->" + target + ")!", code: this.changes});
  });
})

server.listen(8081, function() {
  console.log('%s listening at %s', server.name, server.url);
});

