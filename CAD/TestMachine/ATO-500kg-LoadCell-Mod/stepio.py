# Shared helpers: load the Open-Pull STEP into a dict of {path: (shape_in_world, label)}
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TopLoc import TopLoc_Location
from OCP.IFSelect import IFSelect_RetDone
import cadquery as cq

STEP = "/Users/philipunlayered3d/Documents/Unlayered 3D/tensile machine cad/Open-Pull/CAD/TestMachine/OpenPull-assembly.step"

def load(path=STEP):
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    r = STEPCAFControl_Reader(); r.SetNameMode(True); r.SetColorMode(True)
    assert r.ReadFile(path) == IFSelect_RetDone
    r.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    out = {}
    def name(lab):
        a = TDataStd_Name()
        return a.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), a) else "?"
    def walk(lab, loc, prefix):
        inst = name(lab)
        if st.IsReference_s(lab):
            ref = TDF_Label(); st.GetReferredShape_s(lab, ref)
            loc = loc * st.GetLocation_s(lab); lab = ref
        p = prefix + "/" + inst if prefix else inst
        if st.IsAssembly_s(lab):
            seq = TDF_LabelSequence(); st.GetComponents_s(lab, seq)
            for i in range(1, seq.Length()+1):
                walk(seq.Value(i), loc, p)
        else:
            out[p] = cq.Shape.cast(st.GetShape_s(lab).Moved(loc))
    roots = TDF_LabelSequence(); st.GetFreeShapes(roots)
    for i in range(1, roots.Length()+1):
        walk(roots.Value(i), TopLoc_Location(), "")
    return out
