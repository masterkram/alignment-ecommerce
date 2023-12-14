class Laptop:
    brand: str
    model: str
    modelNumber: str
    title: str
    price: str
    ratingAvgDisplay: str
    ratingNum: str
    ratingAvg: str
    questionNum: str
    batteryLife: str
    totalStorageCapacity: str
    storageType: str
    operatingSystem: str
    processorCores: str
    processorBrand: str
    processorSpeedBase: str
    processorModel: str
    systemMemoryRam: str
    systemMemoryRamType: str
    graphics: str
    screenSize: str
    screenResolution: str
    screenResolutionName: str
    productWeight: str
    color: str
    numberOfUsbPortsTotal: str
    numberOfUsb2Ports: str
    numberOfUsb3Ports: str
    backlitKeyboard: str
    internetConnectivity: str
    bluetoothEnabled: str
    touchScreen: str
    titleStandard: str
    imageURLs: list[str]
    productURL: str

    def __init__(
        self,
        brand: str,
        model: str,
        modelNumber: str,
        title: str,
        price: str,
        ratingAvgDisplay: str,
        ratingNum: str,
        ratingAvg: str,
        questionNum: str,
        batteryLife: str,
        totalStorageCapacity: str,
        storageType: str,
        operatingSystem: str,
        processorCores: str,
        processorBrand: str,
        processorSpeedBase: str,
        processorModel: str,
        systemMemoryRam: str,
        systemMemoryRamType: str,
        graphics: str,
        screenSize: str,
        screenResolution: str,
        screenResolutionName: str,
        productWeight: str,
        color: str,
        numberOfUsbPortsTotal: str,
        numberOfUsb2Ports: str,
        numberOfUsb3Ports: str,
        backlitKeyboard: str,
        internetConnectivity: str,
        bluetoothEnabled: str,
        touchScreen: str,
        titleStandard: str,
        imageURLs: list[str],
        productURL: str,
    ):
        self.brand = brand
        self.model = model
        self.modelNumber = modelNumber
        self.title = title
        self.price = price
        self.ratingAvgDisplay = ratingAvgDisplay
        self.ratingNum = ratingNum
        self.ratingAvg = ratingAvg
        self.questionNum = questionNum
        self.batteryLife = batteryLife
        self.totalStorageCapacity = totalStorageCapacity
        self.storageType = storageType
        self.operatingSystem = operatingSystem
        self.processorCores = processorCores
        self.processorBrand = processorBrand
        self.processorSpeedBase = processorSpeedBase
        self.processorModel = processorModel
        self.systemMemoryRam = systemMemoryRam
        self.systemMemoryRamType = systemMemoryRamType
        self.graphics = graphics
        self.screenSize = screenSize
        self.screenResolution = screenResolution
        self.screenResolutionName = screenResolutionName
        self.productWeight = productWeight
        self.color = color
        self.numberOfUsbPortsTotal = numberOfUsbPortsTotal
        self.numberOfUsb2Ports = numberOfUsb2Ports
        self.numberOfUsb3Ports = numberOfUsb3Ports
        self.backlitKeyboard = backlitKeyboard
        self.internetConnectivity = internetConnectivity
        self.bluetoothEnabled = bluetoothEnabled
        self.touchScreen = touchScreen
        self.titleStandard = titleStandard
        self.imageURLs = imageURLs
        self.productURL = productURL


def laptopFromJson(json: dict) -> Laptop:
    source = json["_source"]
    return Laptop(
        source["brand"],
        source["model"],
        source["modelNumber"],
        source["title"],
        source["price"],
        source["ratingAvgDisplay"],
        source["ratingNum"],
        source["ratingAvg"],
        source["questionNum"],
        source["batteryLife"],
        source["totalStorageCapacity"],
        source["storageType"],
        source["operatingSystem"],
        source["processorCores"],
        source["processorBrand"],
        source["processorSpeedBase"],
        source["processorModel"],
        source["systemMemoryRam"],
        source["systemMemoryRamType"],
        source["graphics"],
        source["screenSize"],
        source["screenResolution"],
        source["screenResolutionName"],
        source["productWeight"],
        source["color"],
        source["numberOfUsbPortsTotal"],
        source["numberOfUsb2Ports"],
        source["numberOfUsb3Ports"],
        source["backlitKeyboard"],
        source["internetConnectivity"],
        source["bluetoothEnabled"],
        source["touchScreen"],
        source["titleStandard"],
        source["imageURLs"],
        source["productURL"],
    )
