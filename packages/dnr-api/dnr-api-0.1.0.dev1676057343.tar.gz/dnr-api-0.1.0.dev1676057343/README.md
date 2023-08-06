# dnr-api

A Python package for accessing the Department of Natural Resources API programmatically.

## Quick Start

### Install the package

```
pip install Tech_Team/Packages/dnr-api
```

### Accessing data

You can easily download a list of records as a DataFrame. For example, here is the `all_dams()` function:
```python
>>> from dnr_api import dams

>>> df = dams.get_all_dams()
>>> df.head()

   DamID PlanNumber    NIDID                DamName   County                        Stream  ...        Owner_FullName  SWJurisdictionStatus ApprovalStatus RatingC  Longitude   Latitude
0      1    P-20559  NE00001          CARPENTER DAM     York               TR-BEAVER CREEK  ...        Nathan Sandall        Jurisdictional       Approved     3.0 -97.650399  40.883122
1      2     P-9325  NE00002            BJERRUM DAM     York  TR-BIG BLUE RIVER             ...   Virgininia  Keahler        Jurisdictional       Approved     3.0 -97.743475  41.038508
2      3     P-9762  NE00003         RECH SMITH DAM     York  TR-LINCOLN CREEK              ...  Anthony J Winter III        Jurisdictional       Approved     3.0 -97.777434  40.930690
3      4    Removed  Removed                Removed  Removed                       Removed  ...               Removed               Removed        Removed     NaN        NaN        NaN
4      5     P-8948  NE00005  UPPER CLEAR CREEK 1-C     Polk  TR-CLEAR CREEK                ...         APG Farms LLC        Jurisdictional       Approved     3.0 -97.718638  41.170599
```

The list functions handle pagination automatically. So you can easily download larger tables:
```python
>>> len(df)

9936
```

You can also fetch the information for a single dam by passing in the Dam ID. For example:
```python
>>> dams.get_dam(5)

{'DamID': 5,
 'PlanNumber': 'P-8948',
 'NIDID': 'NE00005',
 'DamName': 'UPPER CLEAR CREEK 1-C',
 'County': 'Polk',
 'Stream': 'TR-CLEAR CREEK              ',
 'Downstream_Town': 'ROGERS                      ',
 'Downstream_Distance': 56.0,
 'Designer': 'USDA-NRCS',
 'DamType': 'RE - Earthfill',
 'Purpose': 'I - Irrigation',
 'YearCompleted': '1963',
 'YearModified': None,
 'DamLength': 390.0,
 'DamHeight': 22.0,
 'StructureHeight': 26.0,
 'HydraulicHeight': 21.0,
 'MaxDischarge': 1175.0,
 'MaxStorage': 308.0,
 'NormalStorage': 31.0,
 'NormalSurfaceArea': 10.0,
 'DrainageArea': 1536.0,
 'Hazard': 'Low',
 'EAP': 'Not Required',
 'LastInspectionDate': '2018-05-03T00:00:00',
 'StateRegulatedDam': 'Y',
 'RegulatingAgency': 'NE DNR',
 'EmbankmentVolume': 13000.0,
 'AppropriationNumber': 'A-10082',
 'WaterDivision': '2A',
 'PhysicalStatus': 'Existing',
 'JurisdictionalStatus': 'Jurisdictional',
 'Owner_FullName': ' APG Farms LLC',
 'SWJurisdictionStatus': 'Jurisdictional',
 'ApprovalStatus': 'Approved',
 'RatingC': 3,
 'Longitude': -97.71863774,
 'Latitude': 41.17059886}
```

The advantage of fetching a single object instead of an entire list is that the request will be much faster.
