# POPONG Crawlers

Just some minor web crawlers.

## bills

    cd bills
    cp settings.py.sample settings.py
    python getlist.py
    python parselist.py
    python getpages.py
    python parsepages.py

### Attributes
<table>
<tr>
    <th>name</th>
    <th>description</th>
    <th>type</th>
    <th>values</th>
</tr>
<tr>
    <td>`assembly_id`</td>
    <td>국회 대수</td>
    <td>int</td>
    <td></td>
</tr>
<tr>
    <td>`assembly_meeting_id`</td>
    <td>국회 회의 번호</td>
    <td>int</td>
    <td></td>
</tr>
<tr>
    <td>`bill_id`</td>
    <td>의안 번호</td>
    <td>str</td>
    <td></td>
</tr>
<tr>
    <td>`decision_date`</td>
    <td>의결 일자</td>
    <td>str</td>
    <td></td>
</tr>
<tr>
    <td>`decision_result`</td>
    <td>의결 결과</td>
    <td>str</td>
    <td>대안반영폐기, 부결, 수정가결, 원안가결, 철회, 폐기</td>
</tr>
<tr>
    <td>`has_summaries`</td>
    <td>요약본 유무</td>
    <td>int</td>
    <td>
    0: No summary<br>
    1: Has summary
    </td>
</tr>
<tr>
    <td>`link_id`</td>
    <td>링크 번호</td>
    <td>str</td>
    <td>http://likms.assembly.go.kr/bill/jsp/BillDetail.jsp?bill_id=[link_id]</td>
</tr>
<tr>
    <td>`original_bill_links`</td>
    <td>의안원문링크</td>
    <td>list(str)</td>
    <td></td>
</tr>
<tr>
    <td>`proposer_type`</td>
    <td>제안자 구분</td>
    <td>str</td>
    <td>위원장, 의원, 의장, 정부, 기타</td>
</tr>
<tr>
    <td>`proposer_representative`</td>
    <td>대표 발의자</td>
    <td>str</td>
    <td></td>
</tr>
<tr>
    <td>`proposers`</td>
    <td>발의자명단</td>
    <td>list(str)</td>
    <td></td>
</tr>
<tr>
    <td>`proposed_date`</td>
    <td>제안 일자</td>
    <td>str</td>
    <td>[yy]-[mm]-[dd]</td>
</tr>
<tr>
    <td>`status`</td>
    <td>의안 상태</td>
    <td>int</td>
    <td>
        1: 계류의안<br>
        2: 처리의안
    </td>
</tr>
<tr>
    <td>`status_detail`</td>
    <td>심사진행상태</td>
    <td>str</td>
    <td>공포, 대안반영폐기, 본회의불부의, 본회의의결, 부의가능안건, 소관위심사, 소관위심사보고, 소관위접수, 의안정리, 접수, 정부이송, 철회, 체계자구심사, 체계자구의뢰</td>
</tr>
<tr>
    <td>`summaries`</td>
    <td>요약문</td>
    <td>list(str)</td>
    <td></td>
</tr>
<tr>
    <td>`title`</td>
    <td>의안명</td>
    <td>str</td>
    <td></td>
</tr>
<tr>
    <td>`withdrawers`</td>
    <td>철회요구의원 명단</td>
    <td>list(str)</td>
    <td></td>
</tr>


</table>
## election_commission
Get Korean politicians' data from [Korea Election Commission (중앙선거관리위원회)](http://www.nec.go.kr/).

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
