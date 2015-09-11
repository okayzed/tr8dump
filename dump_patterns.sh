# HARDCODE BACKUP DIR FOR NOW
PTNS=$(for i in BACKUP/*PTN*; do echo $i; done | sort -V)


for ptn in $PTNS; do
  echo $ptn
  python tr8_ptn_reader.py < $ptn
  echo ""
done

