/*
 * traffic_wonder.js
 * Copyright (C) 2016 n3xtchen <echenwen@gmail.com>
 *
 * Distributed under terms of the GPL-2.0 license.
 */

var Sequelize = require('sequelize');

var db = new Sequelize('sqlite:///db/dev.db', {
  dialect: 'sqlite',
  storage: './db/dev.db'
});

var Node = db.define('nodes', {
  id: { type: Sequelize.INTEGER, primaryKey: true},
  name: { type: Sequelize.STRING(25)},
  props: Sequelize.TEXT
}, {
  freezeTableName: true,
  timestamps: false
});

var Link = db.define('links', {
  source: { type: Sequelize.INTEGER, primaryKey: true},
  target: { type: Sequelize.INTEGER, primaryKey: true},
  props: Sequelize.TEXT
}, {
  freezeTableName: true,
  timestamps: false
});

exports.Node = Node;
exports.Link = Link;

