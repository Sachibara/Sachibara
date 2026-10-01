<?php
use CodeIgniter\Router\RouteCollection;
/** @var RouteCollection $routes */
$routes->get('/', 'Maintenance::index');
$routes->post('jobs', 'Maintenance::create', ['filter'=>'csrf']);
$routes->post('jobs/(:num)/status', 'Maintenance::status/$1', ['filter'=>'csrf']);
