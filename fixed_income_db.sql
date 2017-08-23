SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Schema FIXED_INCOME_DB
--
-- # The first module is to establish a databse related to treasury futures
-- This database is used to analyse the data related to fixed income products.
-- 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `FIXED_INCOME_DB` DEFAULT CHARACTER SET utf8 ;
USE `FIXED_INCOME_DB` ;

-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`FI_TTF_DAY_TS`
-- 1. 国债期货时间序列表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FIXED_INCOME_DB`.`FI_TTF_DAY_TS` (
  `trade_date` DATETIME NOT NULL COMMENT '交易日期',
  `code` VARCHAR(45) NOT NULL COMMENT '合约代码',
  `type` VARCHAR(45) NULL COMMENT 'T00,T01 or T02',
  `open` DOUBLE(20,5) NULL COMMENT '开盘价',
  `high` DOUBLE(20,5) NULL COMMENT '最高价',
  `low` DOUBLE(20,5) NULL COMMENT '最低价',
  `close` DOUBLE(20,5) NULL COMMENT '收盘价',
  `settle` DOUBLE(20,5) NULL COMMENT '结算价',
  `volume` DOUBLE(20,5) NULL COMMENT '成交价',
  `oi` DOUBLE(20,5) NULL COMMENT 'open interest 持仓量',
  `dtltd` INTEGER NULL COMMENT '距离最后交易日日期',
  `dtldd` INTEGER NULL COMMENT '距离配对缴款日日期',
  PRIMARY KEY (`trade_date`, `code`))
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COMMENT = 'Treasury Futures daily data';


-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`FI_TTF_INFO`
-- 2. 国债期货合约信息表
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`FI_TTF_INFO`;

CREATE TABLE `fi_ttf_info` (
  `code` varchar(45) NOT NULL COMMENT '交易日期',
  `ipo_date` datetime DEFAULT NULL COMMENT '上市时间',
  `last_trade_date` datetime DEFAULT NULL COMMENT '最后交易日',
  `ld_date` datetime DEFAULT NULL COMMENT '配对缴款日',
  PRIMARY KEY (`code`)
) 
ENGINE=MyISAM DEFAULT CHARSET=utf8;





-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`FI_YTM_TS`
-- 3. 国债到期收益率表（中债估值）
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`FI_YTM_TS` ;
CREATE TABLE `fi_ytm_ts` (
  `trade_date` datetime NOT NULL,
  `code` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `term` double(20,5) DEFAULT NULL COMMENT '待偿期限',
  `close` double(20,5) DEFAULT NULL COMMENT '收盘价',
  PRIMARY KEY (`trade_date`,`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`FI_IND_TS`
-- 4. 中债指数表
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`FI_IND_TS` ;

CREATE TABLE IF NOT EXISTS `FIXED_INCOME_DB`.`FI_IND_TS` (
  `trade_date` DATETIME NOT NULL COMMENT '交易日期',
  `code` VARCHAR(45) NOT NULL COMMENT '指数代码',
  `name` VARCHAR(45) NULL COMMENT '指数名称',
  `value` DOUBLE(20,5) NULL COMMENT '指数值',
  PRIMARY KEY (`code`, `trade_date`)
)ENGINE = MyISAM DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`fi_ttf_db_ts`
-- 5. 国债期货可交割券时间序列表
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`fi_ttf_db_ts` ;
CREATE TABLE `fi_ttf_db_ts` (
  `trade_date` datetime DEFAULT NULL COMMENT '交易日期',
  `nx_cupn_day` datetime DEFAULT NULL COMMENT '下一个付息日',
  `accrued_interest` DOUBLE(20,5) DEFAULT NULL COMMENT '应计利息',
  `modi_dura_cnbd` DOUBLE(20,5) DEFAULT NULL COMMENT '中债修正久期',
  `volume` DOUBLE(20,5) DEFAULT NULL,
  `code` VARCHAR(45) COMMENT '可交割券代码',
  `day` DOUBLE(20,5) DEFAULT NULL COMMENT '剩余天数',
  `dirty_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `yield_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `accrued_days` DOUBLE(20,5) DEFAULT NULL,
  `vobp_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `cnvxty_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `matu_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `net_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `trs_ft_code` VARCHAR(45) COMMENT '国债期货代码',
  `cf` DOUBLE(20,5) DEFAULT NULL,
  `basis` DOUBLE(20,5) DEFAULT NULL,
  `expected_ytm` DOUBLE(20,5) DEFAULT NULL COMMENT '远期收益率',
  `implied_ytm` DOUBLE(20, 5) DEFAULT NULL COMMENT '隐含收益率',
  `net_basis` DOUBLE(20,5) DEFAULT NULL COMMENT '净基差',
  `irr` DOUBLE(20,5) DEFAULT NULL,
  `past_days` INTEGER DEFAULT NULL,
  PRIMARY KEY (`trade_date`,`code`,`trs_ft_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`fi_b_info`
-- 6. 关键债券信息表
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`fi_b_info` ;
CREATE TABLE `fi_b_info` (
  `code` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `ipo_date` datetime DEFAULT NULL,
  `carry_date` datetime DEFAULT NULL,
  `issue_amount` bigint(20) DEFAULT NULL,
  `par` int(11) DEFAULT NULL,
  `frequency` double(20,5) DEFAULT NULL,
  `term` double(20,5) DEFAULT NULL,
  `coupon_rate` double(20,5) DEFAULT NULL,
  `coupon_date_txt` varchar(45) DEFAULT NULL,
  `tax_free` varchar(10) DEFAULT NULL,
  `tax_rate` double(20,5) DEFAULT NULL,
  `maturity_date` datetime DEFAULT NULL,
  `outstanding_balance` double(20,5) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`fi_b_ts`
-- 7. 关键债券时间序列表
-- -----------------------------------------------------
DROP TABLE IF EXISTS `FIXED_INCOME_DB`.`fi_b_ts` ;
CREATE TABLE `fi_b_ts` (
  `trade_date` datetime NOT NULL,
  `code` varchar(45) NOT NULL,
  `yield_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `net_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `dirty_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `modi_dura_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `matu_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `vobp_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `cnvxty_cnbd` DOUBLE(20,5) DEFAULT NULL,
  `accrued_days` INTEGER DEFAULT NULL,
  `nx_cupn_day` datetime DEFAULT NULL,
  `accrued_interest` DOUBLE(20,5) DEFAULT NULL,
  `day` INTEGER DEFAULT NULL COMMENT '剩余天数',
  `volume` DOUBLE(20,5) DEFAULT NULL,
  PRIMARY KEY (`trade_date`,`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`fi_b_ts`
-- 8. 期货公司持仓表
-- -----------------------------------------------------
CREATE TABLE `fi_ft_company_ts` (
  `trade_date` datetime NOT NULL,
  `code` varchar(45) NOT NULL,
  `rank_no` int(11) NOT NULL,
  `volume_member_name` varchar(45) DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `volume_inc` float DEFAULT NULL,
  `long_pos_member_name` varchar(45) DEFAULT NULL,
  `long_pos` float DEFAULT NULL,
  `long_pos_inc` float DEFAULT NULL,
  `short_pos_member_name` varchar(45) DEFAULT NULL,
  `short_pos` float DEFAULT NULL,
  `short_pos_inc` float DEFAULT NULL,
  PRIMARY KEY (`trade_date`,`code`,`rank_no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -----------------------------------------------------
-- Table `FIXED_INCOME_DB`.`fi_int_ts`
-- 9. 利率表
-- -----------------------------------------------------
CREATE TABLE `fi_int_ts` (
  `trade_date` datetime NOT NULL,
  `code` varchar(45) NOT NULL,
  `pre_close` double(20,5) DEFAULT NULL,
  `open` double(20,5) DEFAULT NULL,
  `high` double(20,5) DEFAULT NULL,
  `low` double(20,5) DEFAULT NULL,
  `close` double(20,5) DEFAULT NULL,
  `vwap` double(20,5) DEFAULT NULL,
  `volume` double(20,5) DEFAULT NULL,
  `amt` double(20,5) DEFAULT NULL,
  `dealnum` double(20,5) DEFAULT NULL,
  PRIMARY KEY (`trade_date`,`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
