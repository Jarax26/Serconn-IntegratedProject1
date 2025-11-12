BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "searching_servicecategory" (
	"id"	integer NOT NULL,
	"name"	varchar(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "searching_servicecategory" VALUES (1,'Plomería');
INSERT INTO "searching_servicecategory" VALUES (2,'Electricidad');
INSERT INTO "searching_servicecategory" VALUES (3,'Carpintería');
INSERT INTO "searching_servicecategory" VALUES (4,'Jardinería');
INSERT INTO "searching_servicecategory" VALUES (5,'Limpieza del hogar');
INSERT INTO "searching_servicecategory" VALUES (6,'Transporte');
INSERT INTO "searching_servicecategory" VALUES (7,'Cerrajería');
INSERT INTO "searching_servicecategory" VALUES (8,'Pintura');
INSERT INTO "searching_servicecategory" VALUES (9,'Reparación de electrodomésticos');
INSERT INTO "searching_servicecategory" VALUES (10,'Mecánica automotriz');
INSERT INTO "searching_servicecategory" VALUES (11,'Cuidado de niños');
INSERT INTO "searching_servicecategory" VALUES (12,'Cuidado de mascotas');
INSERT INTO "searching_servicecategory" VALUES (13,'Clases particulares');
INSERT INTO "searching_servicecategory" VALUES (14,'Diseño gráfico');
INSERT INTO "searching_servicecategory" VALUES (15,'Programación y desarrollo web');
INSERT INTO "searching_servicecategory" VALUES (16,'Contabilidad y finanzas');
INSERT INTO "searching_servicecategory" VALUES (17,'Marketing digital');
INSERT INTO "searching_servicecategory" VALUES (18,'Traducción de idiomas');
INSERT INTO "searching_servicecategory" VALUES (19,'Fotografía y video');
INSERT INTO "searching_servicecategory" VALUES (20,'Eventos y catering');
INSERT INTO "searching_servicecategory" VALUES (21,'Construcción y remodelación');
INSERT INTO "searching_servicecategory" VALUES (22,'Belleza y estética');
INSERT INTO "searching_servicecategory" VALUES (23,'Barbería y peluquería');
INSERT INTO "searching_servicecategory" VALUES (24,'Entrenador personal');
INSERT INTO "searching_servicecategory" VALUES (25,'Fisioterapia y rehabilitación');
INSERT INTO "searching_servicecategory" VALUES (26,'Servicios de mudanza');
INSERT INTO "searching_servicecategory" VALUES (27,'Soporte técnico informático');
INSERT INTO "searching_servicecategory" VALUES (28,'Diseño de interiores');
INSERT INTO "searching_servicecategory" VALUES (29,'Consultoría empresarial');
INSERT INTO "searching_servicecategory" VALUES (30,'Seguridad privada');
COMMIT;
