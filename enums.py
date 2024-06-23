from enum import Enum


class TitleEnum(str, Enum):
    ai_automation = "ai_automation"
    backend = "backend"
    crm = "crm"
    data_analytics = "data_analytics"
    data_engineer = "data_engineer"
    data_scientist = "data_scientist"
    devops_sre_platform = "devops_sre_platform"
    embedded = "embedded"
    engineering_manager = "engineering_manager"
    executive = "executive"
    frontend = "frontend"
    fullstack = "fullstack"
    hardware = "hardware"
    mobile = "mobile"
    product_manager = "product_manager"
    product_owner = "product_owner"
    research = "research"
    scrum = "scrum"
    security = "security"
    system_arch = "system_arch"
    technical_support = "technical_support"
    testing = "testing"
    ui_ux = "ui_ux"


class LevelEnum(str, Enum):
    c_level = "c_level"
    director = "director"
    group_product_manager = "group_product_manager"
    intern_level = "intern"
    junior = "junior"
    manager = "manager"
    mid_level = "mid_level"
    principal = "principal"
    senior = "senior"
    senior_manager = "senior_manager"
    senior_principal = "senior_principal"
    senior_staff = "senior_staff"
    staff = "staff"
    team_lead = "team_lead"
    vp = "vp"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class BusinessMarketEnum(str, Enum):
    global_market = "global"
    regional_market = "regional"
    local_market = "local"


class BusinessSizeEnum(str, Enum):
    large = "large"
    medium = "medium"
    small = "small"


class BusinessFocusEnum(str, Enum):
    product = "product"
    software = "software_house"


class BusinessLineEnum(str, Enum):
    b2b = "b2b"
    b2c = "b2c"
    both = "both"


class ProgrammingLanguageEnum(str, Enum):
    javascript = "java_script"
    typescript = "type_script"
    python = "python"
    c_sharp = "c_sharp"
    java = "java"
    php = "php"
    c_plus_plus = "c_cplusplus"
    kotlin = "kotlin"
    swift = "swift"
    dart = "dart"
    go = "go"
    r = "r"
    scala = "scala"
    rust = "rust"
