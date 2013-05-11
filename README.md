# POPONG Crawlers

Just some minor web crawlers.

## election_commission
Get Korean politicians' data from [Korea Election Commission (중앙선거관리위원회)](http://www.nec.go.kr/).

## glossary
Get data for [POPONG Glossary](http://popong.com/glossary).

- [Integrated Legislation Knowledge Management System (입법통합지식관리시스템)](http://likms.assembly.go.kr/) 

        cd glossary/likms.assembly.go.kr
        python crawler.py

- [National Assembly Secretaritat (국회사무처)](http://http://nas.na.go.kr/)

        cd glossary/nas.na.go.kr
        python crawler.py
        python parser.py

## google
Get Google search counts.

## peoplepower 
Get [People Power 21 (열려라국회)](http://www.nec.go.kr/) webpages.

    cd peoplepower
    scrapy crawl peoplepower21

## pledges
Get pledges from [NEC (선거관리위원회)](http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fep%2Fepei01.jsp&topMenuId=EP&secondMenuId=EPEI01&menuId=&statementId=EPEI01_%232&electionCode=2&cityCode=0&proportionalRepresentationCode=0&x=17&y=11) for 19th National Assembly officials.

    cd pledges
    python crawler.py

## rokps
Get Korean politicians' data from [ROKPS(헌정회)](http://www.rokps.or.kr).

    cd rokps
    python crawler.py
    python parser.py

## wikipedia
Get Korean lastnames from Wikipedia.
