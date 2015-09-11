# HARDCODE BACKUP DIR FOR NOW
KITS=$(for i in BACKUP/*KIT*; do echo $i; done | sort -V)


for kit in $KITS; do
  echo $kit
  python tr8_kit_reader.py < $kit
  echo ""
done

