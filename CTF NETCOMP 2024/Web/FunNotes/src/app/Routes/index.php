<?php

use App\Controllers\HomeController;
use App\Controllers\DashboardController;
use App\Router;

$router = new Router();

$router->get('/', HomeController::class, 'index');
$router->get('/login', HomeController::class, 'login');
$router->post('/login', HomeController::class, 'goLogin');
$router->get('/signup', HomeController::class, 'signup');
$router->post('/signup', HomeController::class, 'goSignup');
$router->get('/logout', HomeController::class, 'goLogout');

$router->get('/dashboard', DashboardController::class, 'index');

$router->post('/notes/create', DashboardController::class, 'create_notes');
$router->get('/notes/delete', DashboardController::class, 'delete_notes');
$router->get('/notes/export', DashboardController::class, 'export_notes');

$router->dispatch();
