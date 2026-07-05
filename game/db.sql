create database if not exists Othello;

create table if not exists MTSNode(
id serial primary key,
board_hash text not null,
best_child text references MTSNode(board_hash),
move text not null
);
