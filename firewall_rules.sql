--
-- PostgreSQL database dump
--

\restrict MJabDtNA51Gl8Dc0EwNtICFccjuyTybpHEMWbD2PuvqJgXVoNe4sMzh3p870bxg

-- Dumped from database version 15.14 (Debian 15.14-0+deb12u1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: firewall; Type: SCHEMA; Schema: -; Owner: pi
--

CREATE SCHEMA firewall;


ALTER SCHEMA firewall OWNER TO pi;

--
-- Name: firewall_rules_order_index_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.firewall_rules_order_index_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.firewall_rules_order_index_seq OWNER TO pi;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: firewall_rules; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.firewall_rules (
    id integer NOT NULL,
    enabled boolean DEFAULT true,
    action character varying(10) NOT NULL,
    chain character varying(10) DEFAULT 'INPUT'::character varying NOT NULL,
    source character varying(50),
    source_port character varying(10),
    dest character varying(50),
    dest_port character varying(10),
    protocol character varying(10),
    description text,
    order_index integer DEFAULT nextval('public.firewall_rules_order_index_seq'::regclass),
    user_defined boolean DEFAULT true,
    visible boolean DEFAULT true,
    group_id integer,
    extra jsonb
);


ALTER TABLE public.firewall_rules OWNER TO pi;

--
-- Name: firewall_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.firewall_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.firewall_rules_id_seq OWNER TO pi;

--
-- Name: firewall_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public.firewall_rules_id_seq OWNED BY public.firewall_rules.id;


--
-- Name: firewall_rules id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.firewall_rules ALTER COLUMN id SET DEFAULT nextval('public.firewall_rules_id_seq'::regclass);


--
-- Data for Name: firewall_rules; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY public.firewall_rules (id, enabled, action, chain, source, source_port, dest, dest_port, protocol, description, order_index, user_defined, visible, group_id, extra) FROM stdin;
16	t	DROP	FORWARD	192.168.20.100	\N	213.133.127.247	\N	icmp	Drop ICMP from 192.168.20.100	5	t	t	1	\N
14	t	DROP	FORWARD	192.168.20.100	\N	8.8.8.8	80	\N	Drop 80 to 8.8.8.8	3	t	t	\N	\N
\.


--
-- Name: firewall_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('public.firewall_rules_id_seq', 16, true);


--
-- Name: firewall_rules_order_index_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('public.firewall_rules_order_index_seq', 5, true);


--
-- Name: firewall_rules firewall_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.firewall_rules
    ADD CONSTRAINT firewall_rules_pkey PRIMARY KEY (id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO pi;


--
-- PostgreSQL database dump complete
--

\unrestrict MJabDtNA51Gl8Dc0EwNtICFccjuyTybpHEMWbD2PuvqJgXVoNe4sMzh3p870bxg

