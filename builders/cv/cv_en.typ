#import "template.typ": render
#render(yaml(sys.inputs.at("data", default: "data/cv_en.yaml")))
