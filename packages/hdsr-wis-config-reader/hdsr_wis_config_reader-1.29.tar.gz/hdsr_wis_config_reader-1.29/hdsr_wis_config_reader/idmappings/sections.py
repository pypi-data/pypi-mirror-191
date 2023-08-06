from enum import Enum
from hdsr_wis_config_reader.idmappings.files import IdMapChoices


class SectionTypeChoices(Enum):
    kunstwerken = "KUNSTWERKEN"
    waterstandlocaties = "WATERSTANDLOCATIES"
    mswlocaties = "MSWLOCATIES"
    neerslag = "NEERSLAG"
    waterkwaliteit = "WATERKWALITEIT"

    @classmethod
    def get_all(cls):
        return [x.value for x in cls.__members__.values()]


IDMAP_SECTIONS_MAPPER = {
    IdMapChoices.idmap_opvl_water_hymos.value: {
        SectionTypeChoices.kunstwerken.value: [
            {"section_start": "<!--KUNSTWERK SUBLOCS-->", "section_end": "<!--WATERSTANDSLOCATIES-->"}
        ],
        SectionTypeChoices.waterstandlocaties.value: [
            {"section_start": "<!--WATERSTANDSLOCATIES-->", "section_end": "<!--MSW-->",}
        ],
        SectionTypeChoices.mswlocaties.value: [{"section_start": "<!--MSW-->", "section_end": "<!--NEERSLAG-->",}],
        SectionTypeChoices.neerslag.value: [
            {"section_start": "<!--NEERSLAG-->", "section_end": "<!--WATERKWALITEIT-->",}
        ],
        SectionTypeChoices.waterkwaliteit.value: [
            {"section_start": "<!--WATERKWALITEIT-->", "section_end": "<!--OVERIG-->",}
        ],
    },
    IdMapChoices.idmap_opvl_water.value: {
        SectionTypeChoices.kunstwerken.value: [
            {
                "section_start": "<!--KUNSTWERK SUBLOCS (old CAW id)-->",
                "section_end": "<!--WATERSTANDSLOCATIES (old CAW id)-->",
            },
            {
                "section_start": "<!--KUNSTWERK SUBLOCS (new CAW id)-->",
                "section_end": "<!--WATERSTANDSLOCATIES (new CAW id)-->",
            },
        ],
        SectionTypeChoices.waterstandlocaties.value: [
            {"section_start": "<!--WATERSTANDSLOCATIES (old CAW id)-->", "section_end": "<!--MSW (old CAW id)-->",},
            {"section_start": "<!--WATERSTANDSLOCATIES (new CAW id)-->", "section_end": "<!--MSW (new CAW id)-->",},
        ],
        SectionTypeChoices.mswlocaties.value: [{"section_start": "<!--MSW (new CAW id)-->"}],
    },
}


SECTION_TYPE_PREFIX_MAPPER = {
    SectionTypeChoices.kunstwerken.value: r"KW\d{6}$",
    SectionTypeChoices.waterstandlocaties.value: r"OW\d{6}$",
    SectionTypeChoices.mswlocaties.value: r"(OW|KW)\d{6}$",
    SectionTypeChoices.neerslag.value: r"NS\d{4}$",
    SectionTypeChoices.waterkwaliteit.value: r"WQ\d{6}$",
}